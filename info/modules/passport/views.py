import random
import re

from flask import abort
from flask import current_app
from flask import make_response
from flask import request, jsonify

from info import constants
from info import redis_store
from info.libs.yuntongxun.sms import CCP
from info.utils.response_code import RET
from . import passport_blue
from info.utils.captcha.captcha import captcha


@passport_blue.route('/image_code')
def iamge_code():
    """图片验证码后端实现"""
    # 1.取值（取出前端发过来的图片验证码随机编号
    code_id = request.args.get('code_id', None)
    # 2.判断，校验是否为空
    if not code_id:
        abort(404)
    # 3.生成图片验证码
    name, text, image = captcha.generate_captcha()
    # 4.将验证编号作为键，验证码内容作为值保存在redis中
    try:
        redis_store.setex('imageCodeId_' + code_id, constants.SMS_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        current_app.logger.error(e)
        return make_response(jsonify(errno=RET.DATAERR, errmsg='数据错误'))
    # 5.返回图片验证码
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response


@passport_blue.route('/sms_code', methods=['post'])
def sms_code():
    """短信验证码后端实现"""
    # 1.取值（图片验证码编号，图片验证码内容，手机号）
    print('1111')
    params = request.json
    mobile = params.get('mobile')
    image_code_id = params.get('image_code_id')
    image_code = params.get('image_code')
    print(params)
    # 2.判断是否为空
    if not all([mobile, image_code_id, image_code]):
        return jsonify(errno=RET.DATAERR, errmsg='缺少参数')
    # 3.校验手机号
    if not re.match(r'1[35678][0-9]{9}', mobile):
        return jsonify(error=RET.DATAERR, errmsg='手机号不正确')
    # 4.用图片验证码编号从redis中取出之前的内容，并与现在取出的验证码内容比较
    try:
        real_image_code = redis_store.get('imageCodeId_' + image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='数据库查询错误')
    if image_code.upper() != real_image_code.upper():
        print(image_code)
        print(real_image_code)
        return jsonify(errno=RET.DATAERR, errmsg='验证码错误')
    # 5.生成短信验证码
    messcode = "%06d" % random.randint(0, 999999)
    # 6.将手机号和短信验证码给第三方平台，让其发送
    result = CCP().send_template_sms(mobile, [messcode, constants.SMS_CODE_REDIS_EXPIRES / 60], '1')
    print(result)
    if result != 0:
        return jsonify(errno=RET.DATAERR, errmsg='发送失败')

    # 7.将手机号与短信验证码存入redis中
    try:
        redis_store.set("mobile_" + mobile, messcode)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='数据保存失败')
    # 8.发送成功
    return jsonify(errno=RET.OK, errmsg='发送成功')

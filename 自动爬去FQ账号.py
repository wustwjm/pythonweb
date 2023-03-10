import base64
import re
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from selenium import webdriver
import PIL.Image as image
import randomNumber
import requests
import cv2
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By

from PIL import Image, ImageChops



# 构造滑动轨迹
def get_trace(distance):
    '''
    :param distance: (Int)缺口离滑块的距离
    :return: (List)移动轨迹
    '''

    # 创建存放轨迹信息的列表
    trace = []
    # 设置加速的距离
    faster_distance = distance*(4/5)
    # 设置初始位置、初始速度、时间间隔
    start, v0, t = 0, 1, 2
    # 当尚未移动到终点时
    while start < distance:
        # 如果处于加速阶段
        if start < faster_distance:
            # 设置加速度为2
            a = 1.5
        # 如果处于减速阶段
        else:
            # 设置加速度为-3
            a = -3
        # 移动的距离公式
        move = v0 * t + 1 / 2 * a * t * t
        # 此刻速度
        v = v0 + a * t
        # 重置初速度
        v0 = v
        # 重置起点
        start += move
        # 将移动的距离加入轨迹列表
        trace.append(round(move))
    # 返回轨迹信息
    return trace

# 模拟拖动
def move_to_gap(trace):
    # 得到滑块标签
    slider = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]')
    # 使用click_and_hold()方法悬停在滑块上，perform()方法用于执行
    ActionChains(driver).click_and_hold(slider).perform()
    for x in trace:
        # 使用move_by_offset()方法拖动滑块，perform()方法用于执行
        ActionChains(driver).move_by_offset(xoffset=x, yoffset=0).perform()
    # 模拟人类对准时间
    time.sleep(0.5)
    # 释放滑块
    ActionChains(driver).release().perform()

#打开浏览器
driver = webdriver.Firefox()


driver.implicitly_wait(5)


# 打开网站
driver.get('https://feisu261.xyz/auth/login')

# 点击注册
driver.find_element(By.XPATH, '//*[@id="app"]/section/div/div[1]/div/div[1]/a').click()


time.sleep(3)
name_number = randomNumber.random_number()

# 输入昵称
driver.find_element(By.XPATH, '//*[@id="name"]').send_keys(name_number)

email_number = randomNumber.random_number()
time.sleep(1)
# 输入邮箱
driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(email_number)
time.sleep(1)
# 输入密码
driver.find_element(By.XPATH, '//*[@id="passwd"]').send_keys('qqqqqqqq')
time.sleep(1)
# 重新输入密码
driver.find_element(By.XPATH, '//*[@id="repasswd"]').send_keys('qqqqqqqq')

# 休息2秒
time.sleep(3)

# 点击验证
driver.find_element(By.XPATH, '//*[@id="embed-captcha"]/div/div[2]/div[1]/div[3]').click()
# 休息2秒
time.sleep(4)



###############################





while True:
    # 找到包含 Canvas 元素的 HTML 元素
    canvas_element_full_bg = driver.find_element(By.CLASS_NAME, 'geetest_canvas_fullbg')

    # 执行 JavaScript 代码，获取 Canvas 图像的 base64 编码
    canvas_base64_full_bg = driver.execute_script('return arguments[0].toDataURL("image/png").substring(21);',
                                                  canvas_element_full_bg)

    # 将 base64 编码转换为图片
    image_data_full_bg = base64.b64decode(canvas_base64_full_bg)

    # 保存图片
    with open('fq/canvas_image_full_bg.png', 'wb') as f:
        f.write(image_data_full_bg)
        f.close()
    time.sleep(1)
    # 找到包含 Canvas 元素的 HTML 元素html body div.geetest_fullpage_click.geetest_float.geetest_wind.geetest_slide3 div.geetest_fullpage_click_wrap div.geetest_fullpage_click_box div.geetest_holder.geetest_mobile.geetest_ant.geetest_embed div.geetest_wrap div.geetest_widget div.geetest_window a.geetest_link div.geetest_canvas_img.geetest_absolute div.geetest_slicebg.geetest_absolute canvas.geetest_canvas_bg.geetest_absolute
    canvas_element_bg = driver.find_element(By.CLASS_NAME, 'geetest_canvas_bg')

    # 执行 JavaScript 代码，获取 Canvas 图像的 base64 编码
    canvas_base64_bg = driver.execute_script('return arguments[0].toDataURL("image/png").substring(21);',
                                             canvas_element_bg)

    # 将 base64 编码转换为图片
    image_data_bg = base64.b64decode(canvas_base64_bg)

    # 保存图片
    with open('fq/canvas_image_bg.png', 'wb') as f:
        f.write(image_data_bg)
        f.close()

    time.sleep(1)
    # 加载第一张图片
    img1 = Image.open('fq/canvas_image_full_bg.png')

    # 加载第二张图片
    img2 = Image.open('fq/canvas_image_bg.png')

    # 将第一张图片转换为数组
    arr1 = np.array(img1)

    # 将第二张图片转换为数组
    arr2 = np.array(img2)

    # 找到两个数组不同的位置
    diff = np.where(arr1 != arr2)

    # 将不同之处用一个红色方框标出来
    for coord in zip(diff[0], diff[1]):
        arr1[coord] = [255, 0, 0, 0]  # 红色像素点

    # 将标记后的数组转换为图片
    new_img = Image.fromarray(arr1)

    # 保存新图片
    new_img.save('fq/diff.png')

    time.sleep(2)

    # 打开两个图片
    image1 = Image.open("fq/canvas_image_full_bg.png")
    image2 = Image.open("fq/diff.png")

    # 计算两个图片之间的不同
    diff = ImageChops.difference(image1, image2)

    # 找到不同处的位置
    bbox = diff.getbbox()

    time.sleep(1)

    x = int(bbox[0])

    print(x)


    trace = get_trace(x)
    print(trace)

    move_to_gap(trace)

    # # 计算移动轨迹
    # trace = get_trace(x)
    #
    # print(trace)
    # # 移动滑块
    # move_to_gap(trace)
    # # slider = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]')
    # slider = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]')
    # # 模拟点击并拖动滑块
    # action = ActionChains(driver)
    # time.sleep(0.2)
    # action.click_and_hold(slider).move_by_offset(x, 0).release().perform()




    # print(x)
    #
    # hd = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[1]/div[2]/div[2]')
    #
    # # 滑动
    # action = ActionChains(driver)
    # time.sleep(0.5)
    # # 按住滑块
    # action.click_and_hold(hd).perform()
    # time.sleep(0.2)
    # # 滑动
    # action.move_by_offset(x, 0).perform()
    # time.sleep(0.2)
    # # 松开鼠标
    # action.release(hd).perform()
    #
    # time.sleep(2)
    try:
        time.sleep(3)

        # 点击重试


        driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div/div/div[2]/div[2]/form/div[3]/div/div/div/div[2]/div[1]/div[3]/span[2]').click()
        time.sleep(1.5)

        driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]/div/a[2]').click()

    except Exception as e:
        break






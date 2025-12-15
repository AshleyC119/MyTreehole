from PIL import Image, ImageDraw, ImageFont
import os


# 创建默认头像
def create_default_avatar():
    # 确保目录存在
    os.makedirs('/MyTreehole/media/avatars/default.png', exist_ok=True)

    # 创建300x300的蓝色背景图片
    img = Image.new('RGB', (300, 300), color='#007bff')
    d = ImageDraw.Draw(img)

    # 尝试添加用户图标（如果有字体文件）
    try:
        # 在Windows上可以尝试使用系统字体
        font = ImageFont.truetype("arial.ttf", 100)
        d.text((100, 100), "👤", font=font, fill='white')
    except:
        # 如果找不到字体，画一个简单的圆形
        d.ellipse([50, 50, 250, 250], fill='white')

    # 保存图片
    img.save('media/avatars/default.png')
    print("默认头像已创建！")


if __name__ == '__main__':
    create_default_avatar()
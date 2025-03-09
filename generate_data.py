# 生成示例数据的脚本

from database import generate_sample_data
import logging

if __name__ == '__main__':
    try:
        generate_sample_data()
        print("成功生成100条随机待办事项数据！")
    except Exception as e:
        logging.error(f"生成数据失败: {e}")
# 使用官方 Python 镜像作为基础镜像
FROM python:3.10.14

# 设置工作目录
WORKDIR /app

# # 复制 requirements.txt 文件到容器中
# COPY requirements.txt .

# 复制项目文件到容器中
# COPY /home/role/my_rasa_project/dsp-chatbot /app/dsp-chatbot
COPY . .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt


# 暴露端口
EXPOSE 5005 5006 5055

# 训练模型
# RUN rasa train


#CMD ["sh", "-c", "rasa run --port 5005 --enable-api --cors '*' --debug && rasa run actions --port 5055 --debug"]

# 复制脚本文件
COPY script.sh ./script.sh

# 给脚本添加执行权限
RUN chmod a+x ./script.sh

ENTRYPOINT ["./script.sh"] 

# RUN chmod +x ./script.sh
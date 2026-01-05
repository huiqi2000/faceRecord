# faceRecord
打卡记录
前端 Vue
后端 Flask
数据库 MongoDB



# 1. 先创建本地目录（用于存储 MongoDB 数据，可自定义路径）
mkdir -p /root/data/mongodb/

# 2. 运行容器并挂载数据卷
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v /root/data/mongodb/:/data/db \
  -e MONGO_INITDB_ROOT_USERNAME=root \
  -e MONGO_INITDB_ROOT_PASSWORD=root@202601 \
  mongo:6.0
# 说明：
# -v /root/data/mongodb/:/data/db：主机目录 /root/data/mongodb/ 挂载到容器内 /data/db（MongoDB 数据存储目录）



# 1. 先创建本地目录（用于存储 PostgreSQL 数据，可自定义路径）
mkdir -p /root/data/postgres15.6

# 2. 运行容器并挂载数据卷
docker run -d \
  --name postgres15.6 \
  -p 5432:5432 \
  -v /root/data/postgres15.6:/var/lib/postgresql/data \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root@202601 \
  -e POSTGRES_DB=postgres \
  postgres:15.6

docker run -it \
  --name postgres15.6 \
  -p 5432:5432 \
  -e POSTGRES_USER=root \
  -e POSTGRES_PASSWORD=root@202601 \
  -e POSTGRES_DB=postgres \
  postgres:15.6


docker exec -it postgres15.6 /bin/bash

CREATE TABLE clock_record (
    id serial primary key,  -- 直接使用 serial 类型，无需 int，自动为 int 自增
    record_day date,        -- 打卡日期
    record_time timestamp,       -- 打卡时间
    record_type varchar(10) -- 打卡类型：上班/下班
);


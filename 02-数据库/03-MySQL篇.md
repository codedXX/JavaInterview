# MySQL篇

![MySQL篇](../JavaInterviewImages/mysql-slide-001.png)

## 定位慢查询

<!-- 源 PPTX 第 2 页 -->

存储引擎

SQL执行计划

索引底层数据结构

优化

索引

聚簇和非聚簇索引

SQL优化经验

索引创建原则

索引失效场景

事务相关

事务特性

隔离级别

MVCC

其他面试题

主从同步原理

分库分表

![第 2 页：定位慢查询](../JavaInterviewImages/mysql-slide-002.png)

## MySQL-优化

<!-- 源 PPTX 第 3 页 -->

- 定位慢查询
- SQL执行计划
- 索引
- 存储引擎
- 索引底层数据结构
- 聚簇和非聚簇索引
- 索引创建原则
- 索引失效场景
- SQL优化经验

![第 3 页：MySQL-优化](../JavaInterviewImages/mysql-slide-003.png)

## 在MySQL中，如何定位慢查询?

<!-- 源 PPTX 第 4 页 -->

- 聚合查询
- 多表查询
- 表数据量过大查询
- 深度分页查询
- 表象：页面加载过慢、接口压测响应时间过长（超过1s）

![第 4 页：在MySQL中，如何定位慢查询?](../JavaInterviewImages/mysql-slide-004.png)

## 如何定位慢查询 ?

<!-- 源 PPTX 第 5 页 -->

- **方案一：开源工具**
- 调试工具：Arthas
- 运维工具：Prometheus 、Skywalking

![第 5 页：如何定位慢查询 ?](../JavaInterviewImages/mysql-slide-005.png)

## 如何定位慢查询 ?

<!-- 源 PPTX 第 6 页 -->

- **方案二：MySQL自带慢日志**
- 慢查询日志记录了所有执行时间超过指定参数（long\_query\_time，单位：秒，默认10秒）的所有SQL语句的日志
- 如果要开启慢查询日志，需要在MySQL的配置文件（/etc/my.cnf）中配置如下信息：

```text
# 开启MySQL慢日志查询开关
slow_query_log=1
# 设置慢日志的时间为2秒，SQL语句执行时间超过2秒，就会视为慢查询，记录慢查询日志
long_query_time=2
```

```text
配置完毕之后，通过以下指令重新启动MySQL服务器进行测试，查看慢日志文件中记录的信息 /var/lib/mysql/localhost-slow.log。
```

![第 6 页：如何定位慢查询 ?](../JavaInterviewImages/mysql-slide-006.png)

## 如何定位慢查询?

<!-- 源 PPTX 第 7 页 -->

- 介绍一下当时产生问题的场景（我们当时的一个接口测试的时候非常的慢，压测的结果大概5秒钟）
- 我们系统中当时采用了运维工具（ Skywalking ），可以监测出哪个接口，最终因为是sql的问题
- 在mysql中开启了慢日志查询，我们设置的值就是2秒，一旦sql执行超过2秒就会记录到日志中（调试阶段）

![第 7 页：如何定位慢查询?](../JavaInterviewImages/mysql-slide-007.png)

## 如何定位慢查询?

<!-- 源 PPTX 第 8 页 -->

- 介绍一下当时产生问题的场景（我们当时的一个接口测试的时候非常的慢，压测的结果大概5秒钟）
- 我们系统中当时采用了运维工具（ Skywalking ），可以监测出哪个接口，最终因为是sql的问题
- 在mysql中开启了慢日志查询，我们设置的值就是2秒，一旦sql执行超过2秒就会记录到日志中（调试阶段）

那这个SQL语句执行很慢, 如何分析呢？

- 聚合查询
- 多表查询
- 表数据量过大查询
- 深度分页查询

**SQL执行计划（找到慢的原因）**

![第 8 页：如何定位慢查询?](../JavaInterviewImages/mysql-slide-008.png)

## 一个SQL语句执行很慢, 如何分析

<!-- 源 PPTX 第 9 页 -->

可以采用**EXPLAIN** 或者 **DESC**命令获取 MySQL 如何执行 SELECT 语句的信息

- 直接在select语句之前加上关键字 explain / desc<br>EXPLAIN   SELECT   字段列表   FROM   表名   WHERE  条件 ;
- 语法：

![第 9 页：一个SQL语句执行很慢, 如何分析](../JavaInterviewImages/mysql-slide-009.png)

## 一个SQL语句执行很慢, 如何分析

<!-- 源 PPTX 第 10 页 -->

- possible\_key  当前sql可能会使用到的索引
- key 当前sql实际命中的索引
- key\_len 索引占用的大小
- Extra 额外的优化建议

**通过它们两个查看是否可能会命中索引**

| Extra | 含义 |
| --- | --- |
| Using where; Using Index | 查找使用了索引，需要的数据都在索引列中能找到，不需要回表查询数据 |
| Using index condition | 查找使用了索引，但是需要回表查询数据 |

![第 10 页：一个SQL语句执行很慢, 如何分析](../JavaInterviewImages/mysql-slide-010.png)

## 一个SQL语句执行很慢, 如何分析

<!-- 源 PPTX 第 11 页 -->

- type 这条sql的连接的类型，性能由好到差为NULL、system、const、eq\_ref、ref、range、 index、all
- system：查询系统中的表
- const：根据主键查询
- eq\_ref：主键索引查询或唯一索引查询
- ref：索引查询
- range：范围查询
- index：索引树扫描
- all：全盘扫描

![第 11 页：一个SQL语句执行很慢, 如何分析](../JavaInterviewImages/mysql-slide-011.png)

## 那这个SQL语句执行很慢, 如何分析呢？

<!-- 源 PPTX 第 12 页 -->

- 可以采用MySQL自带的分析工具 EXPLAIN
- 通过key和key\_len检查是否命中了索引（索引本身存在是否有失效的情况）
- 通过type字段查看sql是否有进一步的优化空间，是否存在全索引扫描或全盘扫描
- 通过extra建议判断，是否出现了回表的情况，如果出现了，可以尝试添加索引或修改返回字段来修复

![第 12 页：那这个SQL语句执行很慢, 如何分析呢？](../JavaInterviewImages/mysql-slide-012.png)

## MYSQL支持的存储引擎有哪些, 有什么区别 ?

<!-- 源 PPTX 第 13 页 -->

**存储引擎**就是存储数据、建立索引、更新/查询数据等技术的实现方式 。存储引擎是基于表的，而不是基于库的，所以存储引擎也可被称为表类型。

| 特性 | MyISAM | InnoDB | MEMORY |
| --- | --- | --- | --- |
| 事务安全 | 不支持 | 支持 | 不支持 |
| 锁机制 | 表锁 | 表锁/行锁 | 表锁 |
| 外键 | 不支持 | 支持 | 不支持 |

- MySQL体系结构
- InnoDB存储的特点

![第 13 页：MYSQL支持的存储引擎有哪些, 有什么区别 ?](../JavaInterviewImages/mysql-slide-013.png)

## MySQL体系结构

<!-- 源 PPTX 第 14 页 -->

- 连接层
- 服务层
- 引擎层
- 存储层

![第 14 页：MySQL体系结构](../JavaInterviewImages/mysql-slide-014.png)

## 存储引擎特点

<!-- 源 PPTX 第 15 页 -->

- InnoDB

- 介绍
- InnoDB是一种兼顾高可靠性和高性能的通用存储引擎，在 MySQL 5.5 之后，**InnoDB是默认的 MySQL 存储引擎**。
- 特点
- DML操作遵循ACID模型，支持
- ，提高并发访问性能
- 支持         FOREIGN KEY约束，保证数据的完整性和正确性
- 文件
- xxx.ibd：xxx代表的是表名，innoDB引擎的每张表都会对应这样一个表空间文件，存储该表的表结构（frm、sdi）、数据和索引。
- xxx.frm 存储表结构（MySQL8.0时，合并在表名.ibd中）

事务

行级锁

外键

![第 15 页：存储引擎特点](../JavaInterviewImages/mysql-slide-015.png)

## MYSQL支持的存储引擎有哪些, 有什么区别 ?

<!-- 源 PPTX 第 16 页 -->

- 在mysql中提供了很多的存储引擎，比较常见有InnoDB、MyISAM、Memory
- InnoDB存储引擎是mysql5.5之后是默认的引擎，它支持事务、外键、表级锁和行级锁
- MyISAM是早期的引擎，它不支持事务、只有表级锁、也没有外键，用的不多
- Memory主要把数据存储在内存，支持表级锁，没有外键和事务，用的也不多

存储引擎在mysql的体系结构哪一层，主要特点是什么

- MySQL体系结构
- InnoDB存储的特点

![第 16 页：MYSQL支持的存储引擎有哪些, 有什么区别 ?](../JavaInterviewImages/mysql-slide-016.png)

## 索引在项目中的使用方式

<!-- 源 PPTX 第 17 页 -->

- 一是验证你的项目场景的真实性，二是为了作为深入发问的切入点
- 缓存
- 分布式锁
- 消息队列、延迟队列
- … …

![第 17 页：索引在项目中的使用方式](../JavaInterviewImages/mysql-slide-017.png)

## 了解过索引吗？（什么是索引）

<!-- 源 PPTX 第 18 页 -->

索引（index）是帮助MySQL高效获取数据的数据结构(有序)。在数据之外，数据库系统还维护着满足特定查找算法的数据结构（B+树），这些数据结构以某种方式引用（指向）数据， 这样就可以在这些数据结构上实现高级查找算法，这种数据结构就是索引。

36

22

48

19

33

45

53

17

20

23

索引的底层数据结构了解过嘛 ?

二叉树

B+树

红黑树

B树

![第 18 页：了解过索引吗？（什么是索引）](../JavaInterviewImages/mysql-slide-018.png)

## 数据结构对比

<!-- 源 PPTX 第 19 页 -->

MySQL默认使用的索引底层数据结构是B+树。再聊B+树之前，我们先聊聊二叉树和B树

**二叉搜索树**

**最坏的二叉树**

**红黑树**

36

23

22

48

34

20

33

19

45

53

17

![第 19 页：数据结构对比](../JavaInterviewImages/mysql-slide-019.png)

## 数据结构对比

<!-- 源 PPTX 第 20 页 -->

- B-Tree，B树是一种多叉路衡查找树，相对于二叉树，B树每个节点可以有多个分支，即多叉。
- 以一颗最大度数（max-degree）为5(5阶)的b-tree为例，那这个B树每个节点最多存储4个key

- 数据
- 指针

- 20
- 30
- 62
- 89

- 10
- 15
- 18

- 23
- 25
- 28

- 34
- 56
- 58

- 64
- 78
- 88

- 92
- 96
- 98

- 3
- 4

- 11
- 12

13

16

17

- 19
- 20

![第 20 页：数据结构对比](../JavaInterviewImages/mysql-slide-020.png)

## 数据结构对比

<!-- 源 PPTX 第 21 页 -->

B+Tree是在BTree基础上的一种优化，使其更适合实现外存储索引结构，InnoDB存储引擎就是用B+Tree实现其索引结构

- 数据
- 指针
- 键值
- 38
- 67
- 16
- 29
- 55
- 58
- 90
- 94
- 6
- 12
- 16
- 18
- 29
- 34
- 38
- 45
- 55
- 56
- 58
- 62
- 67
- 87
- 90
- 92
- 94
- 98

- B树与B+树对比:
- ①：磁盘读写代价B+树更低；②：查询效率B+树更加稳定；③：B+树便于扫库和区间查询

![第 21 页：数据结构对比](../JavaInterviewImages/mysql-slide-021.png)

## 了解过索引吗？（什么是索引）

<!-- 源 PPTX 第 22 页 -->

- 索引（index）是帮助MySQL高效获取数据的数据结构(有序)
- 提高数据检索的效率，降低数据库的IO成本（不需要全表扫描）
- 通过索引列对数据进行排序，降低数据排序的成本，降低了CPU的消耗

索引的底层数据结构了解过嘛 ?

- MySQL的InnoDB引擎采用的B+树的数据结构来存储索引
- 阶数更多，路径更短
- 磁盘读写代价B+树更低，非叶子节点只存储指针，叶子阶段存储数据
- B+树便于扫库和区间查询，叶子节点是一个双向链表

![第 22 页：了解过索引吗？（什么是索引）](../JavaInterviewImages/mysql-slide-022.png)

## 什么是聚簇索引什么是非聚簇索引 ?

<!-- 源 PPTX 第 23 页 -->

- 什么是聚集索引，什么是二级索引（非聚集索引）
- 什么是回表？

| 分类 | 含义 | 特点 |
| --- | --- | --- |
| 聚集索引(Clustered Index) | 将数据存储与索引放到了一块，索引结构的叶子节点保存了行数据 | 必须有,而且只有一个 |
| 二级索引(Secondary Index) | 将数据与索引分开存储，索引结构的叶子节点关联的是对应的主键 | 可以存在多个 |

- 聚集索引选取规则:
- 如果存在主键，主键索引就是聚集索引。
- 如果不存在主键，将使用第一个唯一（UNIQUE）索引作为聚集索引。
- 如果表没有主键，或没有合适的唯一索引，则InnoDB会自动生成一个rowid作为隐藏的聚集索引。

![第 23 页：什么是聚簇索引什么是非聚簇索引 ?](../JavaInterviewImages/mysql-slide-023.png)

## 什么是聚簇索引和非聚簇索引 ?

<!-- 源 PPTX 第 24 页 -->

聚集索引

二级索引

![第 24 页：什么是聚簇索引和非聚簇索引 ?](../JavaInterviewImages/mysql-slide-024.png)

## 回表查询

<!-- 源 PPTX 第 25 页 -->

```text
select * from user where name = ‘Arm’;
```

聚集索引

回表查询

二级索引

![第 25 页：回表查询](../JavaInterviewImages/mysql-slide-025.png)

## 什么是聚簇索引什么是非聚簇索引 ?

<!-- 源 PPTX 第 26 页 -->

- 聚簇索引（聚集索引）：数据与索引放到一块，B+树的叶子节点保存了整行数据，有且只有一个
- 非聚簇索引（二级索引）：数据与索引分开存储，B+树的叶子节点保存对应的主键，可以有多个

知道什么是回表查询嘛 ?

通过二级索引找到对应的主键值，到聚集索引中查找整行数据，这个过程就是回表

![第 26 页：什么是聚簇索引什么是非聚簇索引 ?](../JavaInterviewImages/mysql-slide-026.png)

## 知道什么叫覆盖索引嘛 ?

<!-- 源 PPTX 第 27 页 -->

**覆盖索引**是指查询使用了索引，并且需要返回的列，在该索引中已经全部能够找到 。

| id | name | gender | createdate |
| --- | --- | --- | --- |
| 2 | Arm | 1 | 2021-01-01 |
| 3 | Lily | 0 | 2021-05-01 |
| 5 | Rose | 0 | 2021-02-14 |
| 6 | Zoo | 1 | 2021-06-01 |
| 8 | Doc | 1 | 2021-03-08 |
| 11 | Lee | 1 | 2020-12-03 |

- id为主键，默认是主键索引
- name字段为普通索引

```text
select * from tb_user where id = 1
select id，name from tb_user where name = ‘Arm’
select id，name，gender from tb_user where name = ‘Arm’
```

覆盖索引

**非覆盖索引(需要回表查询)**

![第 27 页：知道什么叫覆盖索引嘛 ?](../JavaInterviewImages/mysql-slide-027.png)

## 覆盖索引

<!-- 源 PPTX 第 28 页 -->

覆盖索引是指 查询使用了索引，并且需要返回的列，在该索引中已经全部能够找到 。

| id | name | gender | createdate |
| --- | --- | --- | --- |
| 2 | Arm | 1 | 2021-01-01 |
| 3 | Lily | 0 | 2021-05-01 |
| 5 | Rose | 0 | 2021-02-14 |
| 6 | Zoo | 1 | 2021-06-01 |
| 8 | Doc | 1 | 2021-03-08 |
| 11 | Lee | 1 | 2020-12-03 |

5

8

聚集索引(id)

2

3

6

11

row

```text
select  *  from  tb_user  where  id  =  2 ;
```

Lee

Rose

辅助索引(name)

Arm

Doc

Lily

Zoo

![第 28 页：覆盖索引](../JavaInterviewImages/mysql-slide-028.png)

## 覆盖索引

<!-- 源 PPTX 第 29 页 -->

覆盖索引是指 查询使用了索引，并且需要返回的列，在该索引中已经全部能够找到 。

| id | name | gender | createdate |
| --- | --- | --- | --- |
| 2 | Arm | 1 | 2021-01-01 |
| 3 | Lily | 0 | 2021-05-01 |
| 5 | Rose | 0 | 2021-02-14 |
| 6 | Zoo | 1 | 2021-06-01 |
| 8 | Doc | 1 | 2021-03-08 |
| 11 | Lee | 1 | 2020-12-03 |

5

8

聚集索引(id)

2

3

6

11

row

```text
select  *  from  tb_user  where  id  =  2 ;
```

Lee

Rose

辅助索引(name)

```text
select  id, name  from  tb_user  where  name = ‘Arm’ ;
```

Arm

Doc

Lily

Zoo

![第 29 页：覆盖索引](../JavaInterviewImages/mysql-slide-029.png)

## 覆盖索引

<!-- 源 PPTX 第 30 页 -->

覆盖索引是指 查询使用了索引，并且需要返回的列，在该索引中已经全部能够找到 。

| id | name | gender | createdate |
| --- | --- | --- | --- |
| 2 | Arm | 1 | 2021-01-01 |
| 3 | Lily | 0 | 2021-05-01 |
| 5 | Rose | 0 | 2021-02-14 |
| 6 | Zoo | 1 | 2021-06-01 |
| 8 | Doc | 1 | 2021-03-08 |
| 11 | Lee | 1 | 2020-12-03 |

5

8

聚集索引(id)

2

3

6

11

row

```text
select  *  from  tb_user  where  id  =  2 ;
```

**回表 查询**

Lee

Rose

辅助索引(name)

```text
select  id, name  from  tb_user  where  name = ‘Arm’ ;
```

Arm

Doc

Lily

Zoo

```text
select  id,name,gender  from  tb_user  where  name = ‘Arm’ ;
```

**id=2**

![第 30 页：覆盖索引](../JavaInterviewImages/mysql-slide-030.png)

## 知道什么叫覆盖索引嘛 ?

<!-- 源 PPTX 第 31 页 -->

- 覆盖索引是指查询使用了索引，返回的列，必须在索引中全部能够找到
- 使用id查询，直接走聚集索引查询，一次索引扫描，直接返回数据，性能高。
- 如果返回的列中没有创建索引，有可能会触发回表查询，尽量避免使用select \*

MYSQL超大分页怎么处理 ?

可以使用覆盖索引解决

![第 31 页：知道什么叫覆盖索引嘛 ?](../JavaInterviewImages/mysql-slide-031.png)

## MYSQL超大分页处理

<!-- 源 PPTX 第 32 页 -->

- 在数据量比较大时，如果进行limit分页查询，在查询时，越往后，分页查询效率越低。
- 我们一起来看看执行limit分页查询耗时对比：

因为，当在进行分页查询时，如果执行 limit 9000000,10 ，此时需要MySQL排序前9000010 记录，仅仅返回 9000000 - 9000010 的记录，其他记录丢弃，查询排序的代价非常大 。

![第 32 页：MYSQL超大分页处理](../JavaInterviewImages/mysql-slide-032.png)

## MYSQL超大分页处理

<!-- 源 PPTX 第 33 页 -->

优化思路: 一般分页查询时，通过创建 **覆盖索引 **能够比较好地提高性能，可以通过**覆盖索引**加**子查询**形式进行优化

```text
select *
from tb_sku t,
     (select id from tb_sku order by id limit 9000000,10) a
where t.id = a.id;
```

![第 33 页：MYSQL超大分页处理](../JavaInterviewImages/mysql-slide-033.png)

## 知道什么叫覆盖索引嘛 ?

<!-- 源 PPTX 第 34 页 -->

- 覆盖索引是指查询使用了索引，返回的列，必须在索引中全部能够找到
- 使用id查询，直接走聚集索引查询，一次索引扫描，直接返回数据，性能高。
- 如果返回的列中没有创建索引，有可能会触发回表查询，尽量避免使用select \*

MYSQL超大分页怎么处理 ?

- 问题：在数据量比较大时，limit分页查询，需要对数据进行排序，效率低
- 解决方案：覆盖索引+子查询

![第 34 页：知道什么叫覆盖索引嘛 ?](../JavaInterviewImages/mysql-slide-034.png)

## 索引创建原则有哪些？

<!-- 源 PPTX 第 35 页 -->

- 先陈述自己在实际的工作中是怎么用的
- 主键索引
- 唯一索引
- 根据业务创建的索引(复合索引)

![第 35 页：索引创建原则有哪些？](../JavaInterviewImages/mysql-slide-035.png)

## 索引创建原则有哪些？

<!-- 源 PPTX 第 36 页 -->

- 1). 针对于数据量较大，且查询比较频繁的表建立索引。
- 2). 针对于常作为查询条件（where）、排序（order by）、分组（group by）操作的字段建立索引。
- 3). 尽量选择区分度高的列作为索引，尽量建立唯一索引，区分度越高，使用索引的效率越高。
- 4). 如果是字符串类型的字段，字段的长度较长，可以针对于字段的特点，建立前缀索引。
- 5). 尽量使用联合索引，减少单列索引，查询时，联合索引很多时候可以覆盖索引，节省存储空间，避免回表，提高查询效率。
- 6). 要控制索引的数量，索引并不是多多益善，索引越多，维护索引结构的代价也就越大，会影响增删改的效率。
- 7). 如果索引列不能存储NULL值，请在创建表时使用NOT NULL约束它。当优化器知道每列是否包含NULL值时，它可以更好地确定哪个索引最有效地用于查询。

**单表超过10万数据（增加用户体验）**

![第 36 页：索引创建原则有哪些？](../JavaInterviewImages/mysql-slide-036.png)

## 索引创建原则有哪些？

<!-- 源 PPTX 第 37 页 -->

- 1). 数据量较大，且查询比较频繁的表
- 2). 常作为查询条件、排序、分组的字段
- 3). 字段内容区分度高
- 4). 内容较长，使用前缀索引
- 5). 尽量联合索引
- 6). 要控制索引的数量
- 7). 如果索引列不能存储NULL值，请在创建表时使用NOT NULL约束它

**重要**

![第 37 页：索引创建原则有哪些？](../JavaInterviewImages/mysql-slide-037.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 38 页 -->

- 索引失效的情况有很多，可以说一些自己遇到过的，不要张口就得得得说一堆背诵好的面试题
- （适当的思考一下，回想一下，更真实）

给tb\_seller创建联合索引，字段顺序：name，status，address

那快读判断索引是否失效了呢？

**执行计划explain**

![第 38 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-038.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 39 页 -->

- 1). 违反最左前缀法则
- 如果索引了多列，要遵守最左前缀法则。指的是查询从索引的最左前列开始，并且不跳过索引中的列。匹配最左前缀法则，走索引：

![第 39 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-039.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 40 页 -->

违法最左前缀法则 ， 索引失效：

如果符合最左法则，但是出现跳跃某一列，只有最左列索引生效：

![第 40 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-040.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 41 页 -->

2). 范围查询右边的列，不能使用索引 。

根据前面的两个字段 name ， status 查询是走索引的， 但是最后一个条件address 没有用到索引。

![第 41 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-041.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 42 页 -->

3). 不要在索引列上进行运算操作， 索引将失效。

![第 42 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-042.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 43 页 -->

4). 字符串不加单引号，造成索引失效。

由于，在查询是，没有对字符串加单引号， MySQL的查询优化器，会自动的进行类型转换，造成索引失效。

![第 43 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-043.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 44 页 -->

5).以%开头的Like模糊查询，索引失效。如果仅仅是尾部模糊匹配，索引不会失效。如果是头部模糊匹配，索引失效。

![第 44 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-044.png)

## 什么情况下索引会失效 ?

<!-- 源 PPTX 第 45 页 -->

- 违反最左前缀法则
- 范围查询右边的列，不能使用索引
- 不要在索引列上进行运算操作， 索引将失效
- 字符串不加单引号，造成索引失效。(类型转换)
- 以%开头的Like模糊查询，索引失效

![第 45 页：什么情况下索引会失效 ?](../JavaInterviewImages/mysql-slide-045.png)

## 谈一谈你对sql的优化的经验

<!-- 源 PPTX 第 46 页 -->

- 表的设计优化
- 索引优化
- SQL语句优化
- 主从复制、读写分离
- 分库分表

**参考优化创建原则和索引失效**

**后面有专门章节介绍**

![第 46 页：谈一谈你对sql的优化的经验](../JavaInterviewImages/mysql-slide-046.png)

## 谈谈你对sql的优化的经验

<!-- 源 PPTX 第 47 页 -->

- **表的设计优化（参考阿里开发手册《嵩山版》）**
- 比如设置合适的数值（tinyint   int   bigint），要根据实际情况选择
- 比如设置合适的字符串类型（char和varchar）char定长效率高，varchar可变长度，效率稍低

- **SQL语句优化**
- SELECT语句务必指明字段名称（避免直接使用select \* ）
- SQL语句要避免造成索引失效的写法
- 尽量用union all代替union   union会多一次过滤，效率低
- 避免在where子句中对字段进行表达式操作
- Join优化 能用innerjoin 就不用left join right join，如必须使用 一定要以小表为驱动，
- 内连接会对两个表进行优化，优先把小表放到外边，把大表放到里边。left join 或 right join，不会重新调整顺序

```text
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 1000; j++) {
        
    }
}
```

```text
select * from t_user where id > 2
union all  | union
select * from t_user where id < 5
```

![第 47 页：谈谈你对sql的优化的经验](../JavaInterviewImages/mysql-slide-047.png)

## 谈谈你对sql的优化的经验

<!-- 源 PPTX 第 48 页 -->

- **主从复制、读写分离**
- 如果数据库的使用场景读的操作比较多的时候，为了避免写的操作所造成的性能影响 可以采用读写分离的架构。
- 读写分离解决的是，数据库的写入，影响了查询的效率。

- 应用
- 数据库中间件
- DB
- DB
- Master
- Slave
- Write
- Read
- 同步

![第 48 页：谈谈你对sql的优化的经验](../JavaInterviewImages/mysql-slide-048.png)

## 谈一谈你对sql的优化的经验

<!-- 源 PPTX 第 49 页 -->

- 表的设计优化，数据类型的选择
- 索引优化，索引创建原则
- sql语句优化，避免索引失效，避免使用select \*  ….
- 主从复制、读写分离，不让数据的写入，影响读操作
- 分库分表

![第 49 页：谈一谈你对sql的优化的经验](../JavaInterviewImages/mysql-slide-049.png)

## MySQL-其他面试题

<!-- 源 PPTX 第 50 页 -->

- 事务相关
- 主从同步原理
- 其他面试题
- 事务特性
- 隔离级别
- MVCC
- 分库分表

![第 50 页：MySQL-其他面试题](../JavaInterviewImages/mysql-slide-050.png)

## 事务的特性是什么？可以详细说一下吗？

<!-- 源 PPTX 第 51 页 -->

**ACID**

事务是一组操作的集合，它是一个不可分割的工作单位，事务会把所有的操作作为一个整体一起向系统提交或撤销操作请求，即这些操作要么同时成功，要么同时失败。

| id | name | money |
| --- | --- | --- |
| 1 | 张三 | 2000 |
| 2 | 李四 | 2000 |

| id | name | money |
| --- | --- | --- |
| 1 | 张三 | 1000 |
| 2 | 李四 | 3000 |

![第 51 页：事务的特性是什么？可以详细说一下吗？](../JavaInterviewImages/mysql-slide-051.png)

## ACID是什么？可以详细说一下吗？

<!-- 源 PPTX 第 52 页 -->

- 原子性（**A**tomicity）：事务是不可分割的最小操作单元，要么全部成功，要么全部失败。
- 一致性（**C**onsistency）：事务完成时，必须使所有的数据都保持一致状态。
- 隔离性（**I**solation）：数据库系统提供的隔离机制，保证事务在不受外部并发操作影响的独立环境下运行。
- 持久性（**D**urability）：事务一旦提交或回滚，它对数据库中的数据的改变就是永久的。

![第 52 页：ACID是什么？可以详细说一下吗？](../JavaInterviewImages/mysql-slide-052.png)

## 事务的特性是什么？可以详细说一下吗？

<!-- 源 PPTX 第 53 页 -->

- 原子性( Atomicity )
- 一致性( Consistency )
- 隔离性( Isolation )
- 持久性( Durability )
- 结合转账案例进行说明

![第 53 页：事务的特性是什么？可以详细说一下吗？](../JavaInterviewImages/mysql-slide-053.png)

## 并发事务带来哪些问题？怎么解决这些问题呢？MySQL的默认隔离级别是？

<!-- 源 PPTX 第 54 页 -->

- 并发事务问题：脏读、不可重复读、幻读
- 隔离级别：读未提交、读已提交、**可重复读**、串行化

![第 54 页：并发事务带来哪些问题？怎么解决这些问题呢？MySQL的默认隔离级别是？](../JavaInterviewImages/mysql-slide-054.png)

## 并发事务问题

<!-- 源 PPTX 第 55 页 -->

| 问题 | 描述 |
| --- | --- |
| 脏读 | 一个事务读到另外一个事务还没有提交的数据。 |
| 不可重复读 | 一个事务先后读取同一条记录，但两次读取的数据不同，称之为不可重复读。 |
| 幻读 | 一个事务按照条件查询数据时，没有对应的数据行，但是在插入数据时，又发现这行数据已经存在，好像出现了”幻影”。 |

DB

- 2
- 1
- 3
- 事务A

id=1 **(select)**

- 2
- 1
- 3
- 事务B

**脏读**

id=1 **(update)**

![第 55 页：并发事务问题](../JavaInterviewImages/mysql-slide-055.png)

## 并发事务问题

<!-- 源 PPTX 第 56 页 -->

| 问题 | 描述 |
| --- | --- |
| 脏读 | 一个事务读到另外一个事务还没有提交的数据。 |
| 不可重复读 | 一个事务先后读取同一条记录，但两次读取的数据不同，称之为不可重复读。 |
| 幻读 | 一个事务按照条件查询数据时，没有对应的数据行，但是在插入数据时，又发现这行数据已经存在，好像出现了”幻影”。 |

- 2
- 1
- 3
- 事务A
- 4

- 2
- 1
- 3
- 事务B

id=1**(select)**

DB

commit

id=1 **(update)**

**不可重复读**

![第 56 页：并发事务问题](../JavaInterviewImages/mysql-slide-056.png)

## 并发事务问题

<!-- 源 PPTX 第 57 页 -->

| 问题 | 描述 |
| --- | --- |
| 脏读 | 一个事务读到另外一个事务还没有提交的数据。 |
| 不可重复读 | 一个事务先后读取同一条记录，但两次读取的数据不同，称之为不可重复读。 |
| 幻读 | 一个事务按照条件查询数据时，没有对应的数据行，但是在插入数据时，又发现这行数据已经存在，好像出现了”幻影”。 |

- 2
- 1
- 3
- 事务A
- 4

id=1 **(select)**

id=1**(insert)**

- 1
- 事务B
- id=1**(insert)**

DB

commit

**幻读**

![第 57 页：并发事务问题](../JavaInterviewImages/mysql-slide-057.png)

## 怎么解决并发事务的问题呢？

<!-- 源 PPTX 第 58 页 -->

解决方案：对事务进行隔离

| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
| --- | --- | --- | --- |
| Read uncommitted 未提交读 | √ | √ | √ |
| Read committed 读已提交 | × | √ | √ |
| Repeatable Read(默认) 可重复读 | × | × | √ |
| Serializable 串行化 | × | × | × |

注意：事务隔离级别越高，数据越安全，但是性能越低。

![第 58 页：怎么解决并发事务的问题呢？](../JavaInterviewImages/mysql-slide-058.png)

## 并发事务带来哪些问题？怎么解决这些问题呢？MySQL的默认隔离级别是？

<!-- 源 PPTX 第 59 页 -->

- **并发事务的问题：**
- 脏读：一个事务读到另外一个事务还没有提交的数据。
- 不可重复读：一个事务先后读取同一条记录，但两次读取的数据不同
- 幻读：一个事务按照条件查询数据时，没有对应的数据行，但是在插入数据时，又发现这行数据已经存在，好像出现了”幻影”。
- **隔离级别：**
- READ UNCOMMITTED  未提交读
- READ COMMITTED  读已提交
- REPEATABLE READ  可重复读
- SERIALIZABLE    串行化

**脏读、不可重复读、幻读**

**不可重复读、幻读**

**幻读**

![第 59 页：并发事务带来哪些问题？怎么解决这些问题呢？MySQL的默认隔离级别是？](../JavaInterviewImages/mysql-slide-059.png)

## undo log和redo log的区别

<!-- 源 PPTX 第 60 页 -->

- **缓冲池（buffer pool）**:主内存中的一个区域，里面可以缓存磁盘上经常操作的真实数据，在执行增删改查操作时，先操作缓冲池中的数据（若缓冲池没有数据，则从磁盘加载并缓存），以一定频率刷新到磁盘，从而减少磁盘IO，加快处理速度
- **数据页（page）**:是InnoDB 存储引擎磁盘管理的最小单元，每个页的大小默认为 16KB。页中存储的是行数据

- 内存结构
- 磁盘结构

**Buffer Pool**

```text
update
update
delete
```

commit

**xxx.ibd**

![第 60 页：undo log和redo log的区别](../JavaInterviewImages/mysql-slide-060.png)

## redo log

<!-- 源 PPTX 第 61 页 -->

- 重做日志，记录的是事务提交时数据页的物理修改，是**用来实现事务的持久性**。
- 该日志文件由两部分组成：重做日志缓冲（redo log buffer）以及重做日志文件（redo log file）,前者是在内存中，后者在磁盘中。当事务提交之后会把所有修改信息都存到该日志文件中, 用于在刷新脏页到磁盘,发生错误时, 进行数据恢复使用。

- 内存结构
- 磁盘结构

**Buffer Pool**

**Redolog buffer**

```text
update
update
delete
```

commit

数据页变化

**WAL（Write-Ahead Logging）**

ib\_logfile0/1

**xxx.ibd**

![第 61 页：redo log](../JavaInterviewImages/mysql-slide-061.png)

## undo log

<!-- 源 PPTX 第 62 页 -->

- 回滚日志，用于记录数据被修改前的信息 , 作用包含两个 : **提供回滚** 和 **MVCC**(多版本并发控制) 。undo log和redo log记录物理日志不一样，它是**逻辑日志**。
- 可以认为当delete一条记录时，undo log中会记录一条对应的insert记录，反之亦然，
- 当update一条记录时，它记录一条对应相反的update记录。当执行rollback时，就可以从undo log中的逻辑记录读取到相应的内容并进行回滚。

**undo log可以实现事务的一致性和原子性**

![第 62 页：undo log](../JavaInterviewImages/mysql-slide-062.png)

## undo log和redo log的区别

<!-- 源 PPTX 第 63 页 -->

- redo log: 记录的是数据页的物理变化，服务宕机可用来同步数据
- undo log ：记录的是逻辑日志，当事务回滚时，通过逆操作恢复原来的数据
- redo log保证了事务的持久性，undo log保证了事务的原子性和一致性

![第 63 页：undo log和redo log的区别](../JavaInterviewImages/mysql-slide-063.png)

## undo log和redo log的区别

<!-- 源 PPTX 第 64 页 -->

- redo log: 记录的是数据页的物理变化，服务宕机可用来同步数据
- undo log ：记录的是逻辑日志，当事务回滚时，通过逆操作恢复原来的数据
- redo log保证了事务的持久性，undo log保证了事务的原子性和一致性

好的，事务中的隔离性是如何保证的呢？

- 锁：排他锁（如一个事务获取了一个数据行的排他锁，其他事务就不能再获取该行的其他锁）
- mvcc : 多版本并发控制
- 你解释一下MVCC?

![第 64 页：undo log和redo log的区别](../JavaInterviewImages/mysql-slide-064.png)

## 解释一下MVCC

<!-- 源 PPTX 第 65 页 -->

- 全称 **M**ulti-**V**ersion **C**oncurrency **C**ontrol，多版本并发控制。指维护一个数据的多个版本，使得读写操作没有冲突
- MVCC的具体实现，主要依赖于数据库记录中的**隐式字段**、**undo log日志**、**readView**。

- id
- age
- name
- 30
- A30
- 3

**查询的是哪个事务版本的记录**

![第 65 页：解释一下MVCC](../JavaInterviewImages/mysql-slide-065.png)

## MVCC-实现原理

<!-- 源 PPTX 第 66 页 -->

记录中的隐藏字段

id

age

name

DB\_TRX\_ID

DB\_ROLL\_PTR

DB\_ROW\_ID

| 隐藏字段 | 含义 |
| --- | --- |
| DB_TRX_ID | 最近修改事务ID，记录插入这条记录或最后一次修改该记录的事务ID。 |
| DB_ROLL_PTR | 回滚指针，指向这条记录的上一个版本，用于配合undo log，指向上一个版本。 |
| DB_ROW_ID | 隐藏主键，如果表结构没有指定主键，将会生成该隐藏字段。 |

![第 66 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-066.png)

## MVCC-实现原理

<!-- 源 PPTX 第 67 页 -->

undo log

- 回滚日志，在insert、update、delete的时候产生的便于数据回滚的日志。
- 当insert的时候，产生的undo log日志只在回滚时需要，在事务提交后，可被立即删除。
- 而update、delete的时候，产生的undo log日志不仅在回滚时需要，mvcc版本访问也需要，不会立即被删除。

![第 67 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-067.png)

## MVCC-实现原理

<!-- 源 PPTX 第 68 页 -->

undo log版本链

**记录**

- id
- age
- name
- DB\_TRX\_ID
- DB\_ROLL\_PTR

- 30
- 30
- A30
- 1
- null

3

2

0x00001

**undo log**

- 30
- 30
- A30
- 1
- null
- 0x00001

![第 68 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-068.png)

## MVCC-实现原理

<!-- 源 PPTX 第 69 页 -->

undo log版本链

**记录**

- id
- age
- name
- DB\_TRX\_ID
- DB\_ROLL\_PTR

- 30
- 30
- A30
- 1
- null

3

A3

2

0x00002

0x00001

**undo log**

- 30
- 3
- A30
- 2
- 0x00001
- 0x00002

- 30
- 30
- A30
- 1
- null
- 0x00001

![第 69 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-069.png)

## MVCC-实现原理

<!-- 源 PPTX 第 70 页 -->

undo log版本链

**记录**

- id
- age
- name
- DB\_TRX\_ID
- DB\_ROLL\_PTR

- 30
- 30
- A30
- 1
- null

10

3

A3

2

4

0x00002

0x00003

0x00001

**undo log**

- 30
- 3
- A3
- 3
- 0x00002
- 0x00003

- 30
- 3
- A30
- 2
- 0x00001
- 0x00002

- 30
- 30
- A30
- 1
- null
- 0x00001

不同事务或相同事务对同一条记录进行修改，会导致该记录的undolog生成一条记录版本链表，链表的头部是最新的旧记录，链表尾部是最早的旧记录。

![第 70 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-070.png)

## MVCC-实现原理

<!-- 源 PPTX 第 71 页 -->

- 2
- 1
- 3
- 事务A
- 4
- 1
- 2
- 3
- 4
- DB
- 2
- 1
- 3
- 事务B
- id=1**(select)**
- id=1**(select)**
- commit
- id=1 **(update)**

readview

ReadView（读视图）是 **快照读** SQL执行时MVCC提取数据的依据，记录并维护系统当前活跃的事务（未提交的）id。

- 当前读
- 快照读

读取的是记录的**最新版本**，读取时还要保证其他并发事务不能修改当前记录，会对读取的记录进行加锁。对于我们日常的操作，如：select ... lock in share mode(共享锁)，select ... for update、update、insert、delete(排他锁)都是一种当前读。

- 简单的select（不加锁）就是快照读，快照读，读取的是记录数据的可见版本，有可能是历史数据，不加锁，是非阻塞读。
- Read Committed：每次select，都生成一个快照读。
- Repeatable Read：开启事务后第一个select语句才是快照读的地方。

![第 71 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-071.png)

## MVCC-实现原理

<!-- 源 PPTX 第 72 页 -->

ReadView中包含了四个核心字段：

| 字段 | 含义 |
| --- | --- |
| m_ids | 当前活跃的事务ID集合 |
| min_trx_id | 最小活跃事务ID |
| max_trx_id | 预分配事务ID，当前最大事务ID+1（因为事务ID是自增的） |
| creator_trx_id | ReadView创建者的事务ID |

![第 72 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-072.png)

## MVCC-实现原理

<!-- 源 PPTX 第 73 页 -->

readview

trx\_id：代表是当前事务ID。

①. trx\_id  == creator\_trx\_id ? 可以访问该版本

成立，说明数据是当前这个事务更改的。

成立，说明数据已经提交了。

版本链数据访问规则

②. trx\_id \< min\_trx\_id ? 可以访问该版本

③. trx\_id \> max\_trx\_id ?  **不可以访问该版本**

成立，说明该事务是在ReadView生成后才开启。

成立，说明数据已经提交。

④. min\_trx\_id \<= trx\_id \<= max\_trx\_id ?  如果trx\_id不在m\_ids中是可以访问该版本的

- **不同的隔离级别，生成ReadView的时机不同：**
- **READ COMMITTED ：在事务中每一次执行快照读时生成ReadView。**
- **REPEATABLE READ：仅在事务中第一次执行快照读时生成ReadView，后续复用该ReadView。**

![第 73 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-073.png)

## MVCC-实现原理

<!-- 源 PPTX 第 74 页 -->

readview

**RC隔离级别下，在事务中每一次执行快照读时生成ReadView。**

**RC**

- ReadView
- m\_ids: {3,4,5}
- min\_trx\_id: 3
- max\_trx\_id: 6
- creator\_trx\_id: 5

- ReadView
- m\_ids: {4,5}
- min\_trx\_id: 4
- max\_trx\_id: 6
- creator\_trx\_id: 5

![第 74 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-074.png)

## MVCC-实现原理

<!-- 源 PPTX 第 75 页 -->

readview

- ReadView
- m\_ids: {3,4,5}
- min\_trx\_id: 3
- max\_trx\_id: 6
- creator\_trx\_id: 5

**RC**

- ReadView
- m\_ids: {4,5}
- min\_trx\_id: 4
- max\_trx\_id: 6
- creator\_trx\_id: 5

5

3

6

3,4,5

![第 75 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-075.png)

## MVCC-实现原理

<!-- 源 PPTX 第 76 页 -->

readview

- ReadView
- m\_ids: {3,4,5}
- min\_trx\_id: 3
- max\_trx\_id: 6
- creator\_trx\_id: 5

**RC**

- ReadView
- m\_ids: {4,5}
- min\_trx\_id: 4
- max\_trx\_id: 6
- creator\_trx\_id: 5

5

4

6

4,5

![第 76 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-076.png)

## MVCC-实现原理

<!-- 源 PPTX 第 77 页 -->

readview

**RR隔离级别下，仅在事务中第一次执行快照读时生成ReadView，后续复用该ReadView。**

**RR**

- ReadView
- m\_ids: {3,4,5}
- min\_trx\_id: 3
- max\_trx\_id: 6
- creator\_trx\_id: 5

ReadView(复用)

![第 77 页：MVCC-实现原理](../JavaInterviewImages/mysql-slide-077.png)

## 好的，事务中的隔离性是如何保证的呢？(你解释一下MVCC)

<!-- 源 PPTX 第 78 页 -->

- MySQL中的多版本并发控制。指维护一个数据的多个版本，使得读写操作没有冲突
- **隐藏字段**：
- trx\_id(事务id)，记录每一次操作的事务id，是自增的
- roll\_pointer(回滚指针)，指向上一个版本的事务版本记录地址
- **undo log**：
- 回滚日志，存储老版本数据
- 版本链：多个事务并行操作某一行记录，记录不同事务修改数据的版本，通过roll\_pointer指针形成一个链表
- **readView**解决的是一个事务查询选择版本的问题
  - 根据readView的匹配规则和当前的一些事务id判断该访问那个版本的数据
  - 不同的隔离级别快照读是不一样的，最终的访问的结果不一样
  - RC ：每一次执行快照读时生成ReadView
  - RR：仅在事务中第一次执行快照读时生成ReadView，后续复用

![第 78 页：好的，事务中的隔离性是如何保证的呢？(你解释一下MVCC)](../JavaInterviewImages/mysql-slide-078.png)

## MySQL主从同步原理

<!-- 源 PPTX 第 79 页 -->

- 应用
- 数据库中间件
- DB
- DB
- Master
- Slave
- Write
- Read
- 同步

![第 79 页：MySQL主从同步原理](../JavaInterviewImages/mysql-slide-079.png)

## 主从同步原理

<!-- 源 PPTX 第 80 页 -->

MySQL主从复制的核心就是二进制日志

二进制日志（BINLOG）记录了所有的 DDL（数据定义语言）语句和 DML（数据操纵语言）语句，但不包括数据查询（SELECT、SHOW）语句。

master

slave

- 复制分成三步：
- Master 主库在事务提交时，会把数据变更记录在二进制日志文件 Binlog 中。
- 从库读取主库的二进制日志文件 Binlog ，写入到从库的中继日志 Relay Log 。
- slave重做中继日志中的事件，将改变反映它自己的数据。

```text
insert
```

IOthread

SQLthread

read

- data
- change

write

replay

binlog

Relay log

![第 80 页：主从同步原理](../JavaInterviewImages/mysql-slide-080.png)

## 主从同步原理

<!-- 源 PPTX 第 81 页 -->

- MySQL主从复制的核心就是二进制日志binlog(DDL（数据定义语言）语句和 DML（数据操纵语言）语句)
- 主库在事务提交时，会把数据变更记录在二进制日志文件 Binlog 中。
- 从库读取主库的二进制日志文件 Binlog ，写入到从库的中继日志 Relay Log 。
- 从库重做中继日志中的事件，将改变反映它自己的数据

![第 81 页：主从同步原理](../JavaInterviewImages/mysql-slide-081.png)

## 你们项目用过分库分表吗

<!-- 源 PPTX 第 82 页 -->

- DB
- DB
- DB
- DB

- 应用
- 数据库中间件
- DB
- DB
- Master
- Slave
- Write
- Read
- 同步

**分担了访问压力**

**解决存储压力**

- 分库分表的时机：
- 1，**前提**，项目业务数据逐渐增多，或业务发展比较迅速
- 2，优化已解决不了性能问题（主从读写分离、查询索引…）
- 3，IO瓶颈（磁盘IO、网络IO）、CPU瓶颈（聚合查询、连接数太多）

单表的数据量达**1000W**或**20G**以后

![第 82 页：你们项目用过分库分表吗](../JavaInterviewImages/mysql-slide-082.png)

## 拆分策略

<!-- 源 PPTX 第 83 页 -->

垂直分库

垂直拆分

垂直分表

水平分库

水平拆分

水平分表

![第 83 页：拆分策略](../JavaInterviewImages/mysql-slide-083.png)

## 垂直拆分

<!-- 源 PPTX 第 84 页 -->

- 垂直分库

用户微服务

- tb\_user
- tb\_user\_score

- tb\_order
- tb\_orderdetail

订单微服务

网关

- tb\_sku
- tb\_spu

商品微服务

- **垂直分库**：以表为依据，根据业务将不同表拆分到不同库中。
- 特点：
- 按业务对数据分级管理、维护、监控、扩展
- 在高并发下，提高磁盘IO和数据量连接数

![第 84 页：垂直拆分](../JavaInterviewImages/mysql-slide-084.png)

## 垂直拆分

<!-- 源 PPTX 第 85 页 -->

- 垂直分表

- tb\_sku
- id
- name
- category
- brand
- title
- description

- tb\_sku
- id
- name
- category
- brand
- title

- 1
- 1

- 拆分规则：
- 把不常用的字段单独放在一张表
- 把text，blob等大字段拆分出来放在附表中

- tb\_skudesc
- description
- id

- **垂直分表**：以字段为依据，根据字段属性将不同字段拆分到不同表中。
- 特点：
- 1，冷热数据分离
- 2，减少IO过渡争抢，两表互不影响

![第 85 页：垂直拆分](../JavaInterviewImages/mysql-slide-085.png)

## 水平拆分

<!-- 源 PPTX 第 86 页 -->

- 水平分库

id%3==0

- tb\_order
- tb\_orderdetail

应用

id%3==1

id%3==2

- **水平分库**：将一个库的数据拆分到多个库中。
- 特点：
- 解决了单库大数量，高并发的性能瓶颈问题
- 提高了系统的稳定性和可用性

- 路由规则
- 根据id节点取模
- 按id也就是范围路由，节点1(1-100万 ),节点2(100万-200万)
- …

![第 86 页：水平拆分](../JavaInterviewImages/mysql-slide-086.png)

## 水平拆分

<!-- 源 PPTX 第 87 页 -->

- 水平分表

- id%3==0
- id%3==1
- id%3==2

tb\_order

应用

```text
水平分表：将一个表的数据拆分到多个表中(可以在同一个库内)。
特点：
优化单一表数据量过大而产生的性能问题;
避免IO争抢并减少锁表的几率;
```

![第 87 页：水平拆分](../JavaInterviewImages/mysql-slide-087.png)

## 分库分表的策略有哪些

<!-- 源 PPTX 第 88 页 -->

- 新的问题和新的技术

id%3==0

MyCat

应用程序

id%3==1

id%3==2

- 分库之后的问题：
- 分布式事务一致性问题
- 跨节点关联查询
- 跨节点分页、排序函数
- 主键避重

- 分库分表中间件：
- sharding-sphere
- mycat

![第 88 页：分库分表的策略有哪些](../JavaInterviewImages/mysql-slide-088.png)

## 你们项目用过分库分表吗

<!-- 源 PPTX 第 89 页 -->

- 业务介绍
- 1，根据自己简历上的项目，想一个数据量较大业务（请求数多或业务累积大）
- 2，达到了什么样的量级（单表1000万或超过20G）

- 具体拆分策略
- 1，水平分库，将一个库的数据拆分到多个库中，解决海量数据存储和高并发的问题
- 2，水平分表，解决单表存储和性能的问题
- 3，垂直分库，根据业务进行拆分，高并发下提高磁盘IO和网络连接数
- 4，垂直分表，冷热数据分离，多表互不影响

sharding-sphere、mycat

![第 89 页：你们项目用过分库分表吗](../JavaInterviewImages/mysql-slide-089.png)

## 黑马讲师：涛哥

<!-- 源 PPTX 第 90 页 -->

![第 90 页：黑马讲师：涛哥](../JavaInterviewImages/mysql-slide-090.png)

## 第 91 页

<!-- 源 PPTX 第 91 页 -->

![第 91 页：第 91 页](../JavaInterviewImages/mysql-slide-091.png)

## PPTX 内嵌图片

<details>
<summary>展开查看源 PPTX 内嵌媒体</summary>

![mysql-media-001](../JavaInterviewImages/mysql-media-001.png)

![mysql-media-002](../JavaInterviewImages/mysql-media-002.png)

![mysql-media-003](../JavaInterviewImages/mysql-media-003.svg)

![mysql-media-004](../JavaInterviewImages/mysql-media-004.png)

![mysql-media-005](../JavaInterviewImages/mysql-media-005.png)

![mysql-media-006](../JavaInterviewImages/mysql-media-006.svg)

![mysql-media-007](../JavaInterviewImages/mysql-media-007.png)

![mysql-media-008](../JavaInterviewImages/mysql-media-008.png)

![mysql-media-009](../JavaInterviewImages/mysql-media-009.png)

![mysql-media-010](../JavaInterviewImages/mysql-media-010.svg)

![mysql-media-011](../JavaInterviewImages/mysql-media-011.png)

![mysql-media-012](../JavaInterviewImages/mysql-media-012.png)

![mysql-media-013](../JavaInterviewImages/mysql-media-013.png)

![mysql-media-014](../JavaInterviewImages/mysql-media-014.png)

![mysql-media-015](../JavaInterviewImages/mysql-media-015.png)

![mysql-media-016](../JavaInterviewImages/mysql-media-016.png)

![mysql-media-017](../JavaInterviewImages/mysql-media-017.png)

![mysql-media-018](../JavaInterviewImages/mysql-media-018.png)

![mysql-media-019](../JavaInterviewImages/mysql-media-019.png)

![mysql-media-020](../JavaInterviewImages/mysql-media-020.png)

![mysql-media-021](../JavaInterviewImages/mysql-media-021.png)

![mysql-media-022](../JavaInterviewImages/mysql-media-022.png)

![mysql-media-023](../JavaInterviewImages/mysql-media-023.png)

![mysql-media-024](../JavaInterviewImages/mysql-media-024.png)

![mysql-media-025](../JavaInterviewImages/mysql-media-025.png)

![mysql-media-026](../JavaInterviewImages/mysql-media-026.png)

![mysql-media-027](../JavaInterviewImages/mysql-media-027.png)

![mysql-media-028](../JavaInterviewImages/mysql-media-028.png)

![mysql-media-029](../JavaInterviewImages/mysql-media-029.png)

![mysql-media-030](../JavaInterviewImages/mysql-media-030.png)

![mysql-media-031](../JavaInterviewImages/mysql-media-031.png)

![mysql-media-032](../JavaInterviewImages/mysql-media-032.png)

![mysql-media-033](../JavaInterviewImages/mysql-media-033.png)

![mysql-media-034](../JavaInterviewImages/mysql-media-034.png)

![mysql-media-035](../JavaInterviewImages/mysql-media-035.png)

![mysql-media-036](../JavaInterviewImages/mysql-media-036.png)

![mysql-media-037](../JavaInterviewImages/mysql-media-037.png)

![mysql-media-038](../JavaInterviewImages/mysql-media-038.png)

![mysql-media-039](../JavaInterviewImages/mysql-media-039.png)

![mysql-media-040](../JavaInterviewImages/mysql-media-040.png)

![mysql-media-041](../JavaInterviewImages/mysql-media-041.png)

![mysql-media-042](../JavaInterviewImages/mysql-media-042.png)

![mysql-media-043](../JavaInterviewImages/mysql-media-043.png)

![mysql-media-044](../JavaInterviewImages/mysql-media-044.png)

![mysql-media-045](../JavaInterviewImages/mysql-media-045.png)

![mysql-media-046](../JavaInterviewImages/mysql-media-046.png)

![mysql-media-047](../JavaInterviewImages/mysql-media-047.png)

![mysql-media-048](../JavaInterviewImages/mysql-media-048.png)

![mysql-media-049](../JavaInterviewImages/mysql-media-049.png)

![mysql-media-050](../JavaInterviewImages/mysql-media-050.png)

![mysql-media-051](../JavaInterviewImages/mysql-media-051.png)

![mysql-media-052](../JavaInterviewImages/mysql-media-052.png)

![mysql-media-053](../JavaInterviewImages/mysql-media-053.svg)

![mysql-media-054](../JavaInterviewImages/mysql-media-054.png)

![mysql-media-055](../JavaInterviewImages/mysql-media-055.svg)

![mysql-media-056](../JavaInterviewImages/mysql-media-056.png)

![mysql-media-057](../JavaInterviewImages/mysql-media-057.png)

![mysql-media-058](../JavaInterviewImages/mysql-media-058.png)

![mysql-media-059](../JavaInterviewImages/mysql-media-059.svg)

![mysql-media-060](../JavaInterviewImages/mysql-media-060.png)

![mysql-media-061](../JavaInterviewImages/mysql-media-061.svg)

![mysql-media-062](../JavaInterviewImages/mysql-media-062.png)

![mysql-media-063](../JavaInterviewImages/mysql-media-063.png)

![mysql-media-064](../JavaInterviewImages/mysql-media-064.svg)

![mysql-media-065](../JavaInterviewImages/mysql-media-065.png)

![mysql-media-066](../JavaInterviewImages/mysql-media-066.svg)

![mysql-media-067](../JavaInterviewImages/mysql-media-067.png)

</details>

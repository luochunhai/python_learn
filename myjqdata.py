'''
基本面选股
内容：
        1.1  股票池： 选择中证500为股票池、过滤ST、过滤退市、过滤停牌
        1.2  选择销售毛利率大于70% 的股票列表
        1.3  对1.2股票列表排序 ，选择前50只，不足50只，全部入选
                   按照 ROE从大到小排序 （权重为50），
                   按照总市值从小到大排序（权重为50）
        1.4  每周调换股票池一次
'''
# -*- coding = utf-8 -*-
# 导入函数库
from jqdata import *


# 初始化函数，设定基准等等
def initialize(context):
    # 设定中证500作为基准
    set_benchmark('000905.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)

    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5),
                   type='stock')

    # 每周五运行
    # force=True如果超出每周总交易日个数，则取临近的交易日执行；force=False,若注册回调函数的时间晚于第一次回调的执行时间不会就近执行；默认为True
    run_weekly(market_open, weekday=5)


## 开盘时运行函数
def market_open(context):
    # 筛选过滤股票池
    security_list = pick_security()
    log.info('每周第5个交易日选股，如这周不足5个交易日则取临近交易日，股票池如下：')
    log.info(security_list)


## 筛选过滤股票池
def pick_security():
    # 获取中证500股票池
    security_list = get_index_stocks('000905.XSHG')

    # 获取当前时间数据
    current_data = get_current_data()

    # log.info([stock for stock in security_list if current_data[stock].is_st])
    # 过滤ST
    security_list = [stock for stock in security_list if not current_data[stock].is_st]
    # 过滤退市
    security_list = [stock for stock in security_list if not '退' in current_data[stock].name]
    # 过滤停牌
    security_list = [stock for stock in security_list if not current_data[stock].paused]

    # 选择销售毛利率大于70% 的股票列表
    df = get_fundamentals(query(
        indicator.code, indicator.gross_profit_margin
    ).filter(
        valuation.code.in_(security_list),
        indicator.gross_profit_margin > 70
    ).order_by(
        # 按销售毛利率降序排列
        indicator.gross_profit_margin.desc()
    ))

    # 将DataFrame的股票代码转为列表
    security_list = df['code'].tolist()
    # log.info(security_list)

    # 如不足50只股票，全部入选
    if (len(security_list) <= 50):
        return security_list

    # 股票字典，key是股票代码，value是因子排名，例如{000001.XSHE:10, 000002.XSHE:11｝
    security_dict = {}

    # 按ROE（净资产收益率）降序排列
    roe_df = get_fundamentals(query(
        indicator.code
    ).filter(
        valuation.code.in_(security_list)
    ).order_by(
        indicator.roe.desc()
    ))
    roe_list = roe_df['code'].tolist()  # 得到ROE降序列表
    # log.info(roe_list)

    for i in range(len(roe_list)):
        # 得到ROE权重字典，因i初始为0,固 ROE权重得分 = 排名(i+1) * 权重(0.5)
        security_dict[roe_list[i]] = (i + 1) * 0.5
    # log.info(security_dict)

    # 按照总市值升序排列
    cap_df = get_fundamentals(query(
        indicator.code
    ).filter(
        valuation.code.in_(security_list)
    ).order_by(
        valuation.market_cap.asc()
    ))

    cap_list = cap_df['code'].tolist()  # 得到总市值升序列表
    # log.info(cap_list)

    for i in range(len(cap_list)):
        # 股票权重最终得分 = ROE权重得分 + 总市值得分（排名*0.5)
        security_dict[cap_list[i]] = security_dict[cap_list[i]] + (i + 1) * 0.5
    # log.info(security_dict)

    # 对security_dict字典按value排序，生成的值为列表 例如 [('000002.XSHE', 1.0), ('000001.XSHE', 1.0)] 
    sorted_list = sorted(security_dict.items(), key=lambda x: x[1], reverse=False)  # True是倒叙 默认是False
    sorted_list = sorted_list[:50]  # 取出前50个

    security_list = []
    for i in range(len(sorted_list)):
        security_list.append(sorted_list[i][0])

    return security_list


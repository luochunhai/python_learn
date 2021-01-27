def dayUP(df):
    dayup = 1
    for i in range(365):
        if i % 7 in [0, 6]:
            dayup = dayup * (1 - df)
        else:
            dayup = dayup * (1 + df)
    return dayup


dayFactor = 0.01
while dayUP(dayFactor) < 37.78:
    dayFactor += 0.001

print("result:{:.3f}".format(dayFactor))

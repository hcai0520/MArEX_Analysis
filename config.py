import yaml
filename= 'config/conditions.yml'
with open(filename) as f:
    c= yaml.safe_load(f)
c['empty']['runlist'] = [i for i in range(117348, 117360)] + [i for i in range(117362, 117369)]+ [i for i in range(117429,117436)] + [i for i in range(117444,117449)]+[i for i in range(117543,117547)]+[117452,117739]+[i for i in range(117511,117519)]
c['empty_Bi']['runlist'] = [i for i in range(117369,117398)]+[117436,117437] + [i for i in range(117422,117428)]+ [i for i in range(117439,117444)]
c['empty_Al_8']['runlist'] = [i for i in range(117449,117452)]+[i for i in range(117453,117461)]
c['empty_Al_5']['runlist'] = [i for i in range(117461,117467)]+[i for i in range(117470,117485)]+[i for i in range(117497,117511)]+[i for i in range(117519,117523)]+[i for i in range(117530,117532)]
c['empty_Al_3']['runlist'] = [i for i in range(117485,117494)]+[117496]
c['Carbon']['runlist'] = [i for i in range(117559,117567)]+[i for i in range(117575,117582)]+[117583]
c['Carbon_Al_5']['runlist'] = [i for i in range(117567,117575)]
c['Al_5']['runlist'] = [117584]+[i for i in range(117586,117592)]
c['Bi_1.2']['runlist'] = [i for i in range(117593,117598)]
c['Argon_bottle']['runlist'] = [117665,117680,117688,117714] + [i for i in range(117683,117686)]+[i for i in range(117692,117694)]+[i for i in range(117710,117714)]+[i for i in range(117716,117719)]+[i for i in range(117724,117739)]
c['Air_bottle']['runlist'] = [i for i in range(117746,117758)]+[i for i in range(117761,117468)]




with open(filename, 'w') as f:
    yaml.safe_dump(c,f)
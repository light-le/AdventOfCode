
ymax = -57
ymin = -101
xmax = 286
xmin = 257

'''
vver = h/t + t/2 - 1/2 where t is step and whole, h, vver are also whole, t > 2vver. h is between ymax and ymin
'''
vver_acceptance = []
for h in range(ymin, ymax+1):
    t = 0
    vver = 0
    while vver < abs(ymin):
        t+=1
        vver = h/t + t/2 - 1/2
        if vver.is_integer():
            vver_acceptance.append({
                'vver': vver,
                'h': h,
                't': t,
            })
max_vver = max([v['vver'] for v in vver_acceptance])
highest = max_vver*(max_vver+1)/2
print(highest)

v_acceptance = []
for vver_acc in vver_acceptance:
    t = vver_acc['t']
    h = vver_acc['h']
    vver = vver_acc['vver']
    for vhor in range(23, xmax+1):
        if vhor >= (t-1):
            l = vhor*t - t*(t-1)/2
        else:
            l = vhor*(vhor+1)/2
        if l in range(xmin, xmax+1):
            accept = {
                'vver': vver,
                'vhor': vhor,
                'h': h,
                'l': l,
                't': t
            }
            v_acceptance.append(accept)
unique_v = set([(v['vver'], v['vhor']) for v in v_acceptance])
print(len(unique_v))


print('\n'.join([''.join([('AndyLove'[(x-y) % 8]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3 <= 0 else' ')
                          for x in range(-30,30)])for y in range(15, -15, -1)]))

# print('\n'.join([''.join(['*'if abs((lambda a:lambda z,c,n:a(a,z,c,n))(lambda s,z,c,n:z if n==0else s(s,z*z+c,c,n-1))(0,0.02*x+0.05j*y,40))2 else ' ' for x in range(-80,20)])for y in range(-20,20)]))



# from functools import reduce
#
# a = [{'qty': 2, 'len': 1000}, {'qty': 3, 'len': 5000}, {'qty': 1, 'len': 10000}]
# a_total_len = [x for x in a]
# print(type(a_total_len))
# print(a_total_len)

# list = [1, 2, 3, 4, 5]
# s = reduce(lambda x, y: x + y, list)
# print(s)
# list = [10,6,7,5,2,1,8,5]
# s = reduce(lambda x,y: x if (x > y) else y, list)
# print(s)
# list = [1,2,3,4,5,6,7,8,9,10]
# newList = filter(lambda x: x % 2 == 0, list)
# print(newList)
# list = [1,2,3,4,5]
# squaredList = map(lambda x: x*x, list)
# print(squaredList)
# f = lambda x: x > 10
# print(f(2))
# print(f(12))
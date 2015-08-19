func=Interpolation[{{{0,0,0},0},{{0,0,1},0},{{0,0,2},0},{{0,1,0},0},{{0,1,1},0},{{0,1,2},0},{{0,2,0},0},{{0,2,1},0},{{0,2,2},1},{{1,0,0},0},{{1,0,1},0},{{1,0,2},0},{{1,1,0},1},{{1,1,1},1},{{1,1,2},1},{{1,2,0},1},{{1,2,1},2},{{1,2,2},2},{{2,0,0},1},{{2,0,1},1},{{2,0,2},2},{{2,1,0},3},{{2,1,1},3},{{2,1,2},3},{{2,2,0},3},{{2,2,1},4},{{2,2,2},4}}]
eval=Function[{a,b,c},func[a,b,c]]
da=Function[{a,b,c},Evaluate[D[eval[a,b,c],a]]]
db=Function[{a,b,c},Evaluate[D[eval[a,b,c],b]]]
dc=Function[{a,b,c},Evaluate[D[eval[a,b,c],c]]]
N[da[0,0,0]]
N[da[0,0,1]]
N[da[0,0,2]]
N[da[0,1,0]]
N[da[0,1,1]]
N[da[0,1,2]]
N[da[0,2,0]]
N[da[0,2,1]]
N[da[0,2,2]]
N[da[1,0,0]]
N[da[1,0,1]]
N[da[1,0,2]]
N[da[1,1,0]]
N[da[1,1,1]]
N[da[1,1,2]]
N[da[1,2,0]]
N[da[1,2,1]]
N[da[1,2,2]]
N[da[2,0,0]]
N[da[2,0,1]]
N[da[2,0,2]]
N[da[2,1,0]]
N[da[2,1,1]]
N[da[2,1,2]]
N[da[2,2,0]]
N[da[2,2,1]]
N[da[2,2,2]]
N[db[0,0,0]]
N[db[0,0,1]]
N[db[0,0,2]]
N[db[0,1,0]]
N[db[0,1,1]]
N[db[0,1,2]]
N[db[0,2,0]]
N[db[0,2,1]]
N[db[0,2,2]]
N[db[1,0,0]]
N[db[1,0,1]]
N[db[1,0,2]]
N[db[1,1,0]]
N[db[1,1,1]]
N[db[1,1,2]]
N[db[1,2,0]]
N[db[1,2,1]]
N[db[1,2,2]]
N[db[2,0,0]]
N[db[2,0,1]]
N[db[2,0,2]]
N[db[2,1,0]]
N[db[2,1,1]]
N[db[2,1,2]]
N[db[2,2,0]]
N[db[2,2,1]]
N[db[2,2,2]]
N[dc[0,0,0]]
N[dc[0,0,1]]
N[dc[0,0,2]]
N[dc[0,1,0]]
N[dc[0,1,1]]
N[dc[0,1,2]]
N[dc[0,2,0]]
N[dc[0,2,1]]
N[dc[0,2,2]]
N[dc[1,0,0]]
N[dc[1,0,1]]
N[dc[1,0,2]]
N[dc[1,1,0]]
N[dc[1,1,1]]
N[dc[1,1,2]]
N[dc[1,2,0]]
N[dc[1,2,1]]
N[dc[1,2,2]]
N[dc[2,0,0]]
N[dc[2,0,1]]
N[dc[2,0,2]]
N[dc[2,1,0]]
N[dc[2,1,1]]
N[dc[2,1,2]]
N[dc[2,2,0]]
N[dc[2,2,1]]
N[dc[2,2,2]]

tree = {
'1' : ['2','3'], '2' : ['4','5'], '3' : ['6','7'],
'4' : ['8'], '5' : ['9','10'], '6' : ['11'],
'7' : ['12'], '8' : [], '9' : [], 
'10' : [], '11' : [], '12' : [],
}
def dfs(source, target, limit):
    print(source,end=' ')
    if source==target:
        return True
    if limit<=0:
        return False
    for i in tree[source]:
        if dfs(i,target,limit-1):
            return True
    return False
def iterative_deepning_search(source,target,maxDepth):
    level=0
    for i in range(0,maxDepth+1):
        print(level," -> ",end=' ')
        level+=1
        if dfs(source,target,i)==True:
            return True
        print()
    return False
if iterative_deepning_search('1','10',3)==True:
    print("\nFound")
else:
    print("\nNot found")
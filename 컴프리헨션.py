# a,b = map(int, input().split())
# print(a+b)
# print(a-b)
# print(a*b)
# print(a//b)


# Gemini의 응답
# '컴프리헨션(Comprehension)'은 영단어 뜻 그대로 해석하면 '이해' 또는 **'포함'**이라는 의미를 갖지만, 파이썬 프로그래밍에서는 **"리스트나 딕셔너리 같은 컬렉션을 빠르고 간결하게 생성하는 문법"**을 뜻합니다.

# 쉽게 말해, 여러 줄의 for문과 if문을 대괄호 [ ] 안에 한 줄로 압축해 넣는 것이라고 이해하시면 됩니다.

# 1. 왜 '컴프리헨션'이라고 부를까요?
# 수학의 **'집합 조건제시법'**에서 아이디어를 가져왔기 때문입니다.

# 수학: A={x∣x는 10보다 작은 짝수}

# 파이썬: A = [x for x in range(10) if x % 2 == 0]


from re import split


# DATA = [list( map( int, input().split())) for _ in  range(5)]

# print(DATA[0])
# print(DATA[1])
# print(DATA[2])
# print(DATA[3])
# print(DATA[4])



# "이런 조건을 **포함(Comprehend)**하고 있는 리스트를 만들어줘!"라고 명령하는 방식인 셈이죠.

apple = ["AAA", "BBB", "CCC"          , "DDD", "EEE"]
print(apple[1:3])
print(apple[-3:-1])

nums = [1900, 8020, 30, 40, 50]
# 1. 처음부터 인덱스 3 미만까지
print(nums[:3])
# 2. 인덱스 2부터
print(nums[2:].sort(reverse=True))
# print(sorted(nums, reverse=True))
print(nums) 
print(nums[2:] , list(map(int, nums[2:])))


data = {'A': 10, 'B': 20} 
print(data['A'])
print(data['B'])
data['C'] = 30
print(data)
data.update({'D': 40})
print(data)

print("%10s" % "goog")
print("%-10s" % "goog")
print(f"{1234567:,}")
pi = 3.141592
print(f"{pi:.2f}")
name = "python"
print(f"{name.upper()}의 길이는 {len(name)}입니다.")
# 결과: PYTHON의 길이는 6입니다.
x= 10
y = 20
print(f"{x=}, {y=}")
print(f"{x=}%")
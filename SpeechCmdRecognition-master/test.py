# f = open('C:/Users/rafoo/Documents/Bigdata/BlockandReplicaStates1.txt','r+')
# f1 =open('C:/Users/rafoo/Documents/Bigdata/2_HDFSClient.txt','w')
#
# lines = f.readlines()
#
# for line in lines:
#     if line[0].isdigit():
#         continue
#     else:
#         f1.write(line)
#
# f.close()
# f1.close()

def change(st):
    lis = list(filter(lambda x: 26 >= x >= 1, [ord(char) - 96 for char in st.lower()]))
    stri = ['0'] * 26


    for i in lis:
        stri[i-1] = '1'

    return "".join(stri)
print(change("a **&  bZ"))


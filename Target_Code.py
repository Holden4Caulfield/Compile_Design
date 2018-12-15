class Target():

    j_w=['_','-','+','*','/','=','>','<','>=','<=','==','ie','el','if','wh','do','we']
    id_list=[]
    lan_block=[]
    Qt_lis=[
        """ ['=','3','_','a'],
        ['=','2','_','b'],
        ['+','a','b','t1'],
        ['*','a','t1','t3'],
        ['/','t3','t1','x'],
        ['=','t1','_','i'] """
    ]
    if_stack=[]
    if_c=0               #计数
    while_c=0
    while_stack=[]
    block_name=''            #给每个语句块定义一个标识符
    def __init__(self):
        self.open_file()
        self.get_list()
        self.prepare()
        self.parse_main()
        pass

    #打开四元式文件,读取四元式存入Qt_lis
    def open_file(self):
        lis=[]
        with open('D:/Compile_Design/esay.txt') as f:
            for line in f:
                lis.append(line.split(' '))
            f.close()
        for item in lis:
            if(len(item)==1):
                continue
            else:
                item[3]=item[3][0:-1]
        self.Qt_lis=lis        


    def prepare(self):
        print('DSEG     SEGMENT')
        for item in self.id_list:
            print(item['name']+'     '+'DW    '+'?')
        print('DSEG     ENDS')
        print('CSEG     SEGMENT')
        print('    ASSUME CS:CSEG,DS:DSEG')    

    #解析语句块
    def parse_block(self,lis_block):
        out_put=[]
        for line in lis_block:
            if self.block_name !='':
                print(self.block_name+':')
                self.block_name=''
            if(len(line)==1):
                continue
            #简单运算
            elif line[0] in ['+','-']:
                if line[0]=='+':
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        ADD   AX,'+str(line[2]))
                    out_put.append('        MOV   '+str(line[3])+','+'AX')
                else:
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        SUB   AX,'+str(line[2]))
                    out_put.append('        MOV   '+str(line[3])+','+'AX')
            elif line[0] in ['*','/']:
                if line[0] == '*':
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        MUL   '+str(line[2]))
                    out_put.append('        MOV   '+str(line[3])+','+'AX')
                else:
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        DIV   '+str(line[2]))
                    out_put.append('        MOV   '+str(line[3]).upper()+','+'AX')
            elif line[0]=='=':

                out_put.append('        MOV   '+'DX'+','+str(line[1]))
                out_put.append('        MOV   '+str(line[3])+','+'DX')   
            #转移指令 JMP
            elif line[0] in ['>=','<=','==','>','<']:
                print(line)
                pass
                
            #包含转移的指令    
            if line[0] in ['if','el','ie','do','we','wh']:
                if line[0]=='wh':
                    self.while_c+=1
                    name='while'+str(self.while_c)
                    self.while_stack.append(name)
                    self.block_name=name
                #do,we 要寻找与之对应的whil，从while栈中栈顶得到    
                if line[0] =='do':
                    name='do'+str(self.while_c)
                    self.block_name=name
                if line[0] == 'we':
                     name='we'+str(self.while_c)
                     self.while_stack.pop()
                     self.block_name=name
                if line[0]=='if':
                    self.if_c+=1
                    name='if'+str(self.if_c)
                    self.if_stack.append(name)
                    self.block_name=name
                #do,we 要寻找与之对应的whil，从while栈中栈顶得到    
                if line[0] =='el':
                    name='else'+str(self.if_c)
                    self.block_name=name
                if line[0] == 'ie':
                     name='ie'+str(self.if_c)
                     self.if_stack.pop()
                     self.block_name=name
                        

               


        for i in out_put:
            print(i)
        pass

    #划分基本块,获得变量表
    def get_list(self):
        #传入四元式,逐条分析
        for items in self.Qt_lis:
            for item in items:
                if item =='\n':
                    continue
                id_dic={}
                #判断是标识符
                if(self.jud_isid(item)):
                    id_dic['name']=item
                    if id_dic in self.id_list:
                        continue
                    self.id_list.append(id_dic)

        print(self.id_list)            
        pass

    def jud_isid(self,word):
        if word in self.j_w:
            return 0
        elif word.isdigit():
            return 0    
        else:
            return 1    



    #分析语句块
    def parse_main(self):

        #基本块 
        print('START: MOV  AX,DSEG')
        print('     MOV  DS,AX')       
        self.cut_block()
        print('CSEG     ENDS')
        print('     END  START')       
        pass
    
    #划分基本块
    def cut_block(self):
        """ for item in self.Qt_lis:
            print(item)
            print('a') """
        lis_block=[]
        for item in self.Qt_lis:
            if len(item) != 1:
                lis_block.append(item)
            else:
                
                #lis_block.append('\n')
                self.parse_block(lis_block)
                lis_block.clear()
        if len(lis_block)!=0:
            
            lis_block.append('end')
            self.parse_block(lis_block)
            lis_block.clear()
                    




if __name__ =='__main__':
    tr=Target()
    print('dong')
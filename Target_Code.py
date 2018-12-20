from newdag import Optimizer
from Digui import MiddleCode
from Digui import SymbolItem
from Digui import MiddleCode
from Digui import TempVar

class Target_fun():
    j_w=['_','-','+','*','/','=','>','<','>=','<=','==','ie','el','if','wh','do','we']
    def __init__(self,lis,f_dic):
        self.dic_clear()
        self.Qt_lis=lis
        self.f_dict=f_dic
        #self.get_list()
        #print(self.id_list)
        self.prepare()
        self.parse_main()
        print(self.rea_dic)
        print(self.off_dic)
        pass     

    def dic_clear(self):
        self.Temp_count=int(0)
        self.f_dict=dict()
        self.off_add=int(0)         #偏移地址
        self.off_dic=dict()         #偏移量建立键值对关系
        self.id_list=list()         #标识符，存偏移地址
        self.lan_block=list()
        self.Qt_lis=list()
        self.if_stack=list()
        self.if_c=int(0)               #计数
        self.while_c=int(0)
        self.while_stack=list()
        self.jm_status=dict()
        self.out_put=list()
        self.rea_dic=dict()            #构建字典，存储转移逻辑
        self.block_name=str('')            #给每个语句块定义一个标识符
        self.fname=str('')



    #控制主DI指针移动
    def control(self,op,num):
        if op == '+':
            for item in self.off_dic.keys():
                self.off_dic[item]=self.off_dic[item]+num
        if op == '-':
            del_lis=[]
            for item in self.off_dic.keys():
                self.off_dic[item]=self.off_dic[item]-num
                if self.off_dic[item] <= 0:
                    del_lis.append(item)
            for item in del_lis:
                del self.off_dic[item]        
                    

        
                

       




    def prepare(self):
        self.fname=self.f_dict['name']   

    #解析语句块
    def parse_block(self,lis_block):
        
        load_name=''
        out_put_block=[]
        logic_op='none'
        sub_tag=0
        for line in lis_block:
            if self.block_name !='':
                out_put_block.append('          SUB     DI'+str(self.Temp_count))
                self.control('-',self.Temp_count)
                self.Temp_count=0
                load_name=self.block_name
                if 'ie' in load_name:
                    #没有else情况下,补充else
                    out_put_block.append('          SUB     DI'+str(self.Temp_count))
                    self.control('-',self.Temp_count)
                    self.Temp_count=0
                    if self.jm_status[self.rea_dic[load_name]] != 'done':
                        self.jm_status[self.rea_dic[load_name]] = 'done'
                        print(self.rea_dic[self.rea_dic[load_name]][-1]+':')
                      
                    pass
                out_put_block.append(self.block_name+':')
                if 'we' in load_name:
                    #print(self.jm_status)
                    #while end 要转移到while开始位置
                    out_put_block.append('          SUB     DI'+str(self.Temp_count))
                    self.control('-',self.Temp_count)
                    self.Temp_count=0
                    if self.jm_status[self.rea_dic[load_name]]=='begin':
                        out_put_block.append('      JMP  '+self.rea_dic[load_name])
                        #out_put_block.append('6666')
                        self.jm_status[self.rea_dic[load_name]]='done'
                
                self.block_name=''
            if line is None:
                continue
            #简单运算,结果保存，存入[DI]
            if line.opt in ['-','+','*','/','=']:
                #运算单元肯定已知，不是标识就是常数,结果肯定是临时变量，不需要存
                if line.opt in ['-','+','*','/']:
                    if isinstance(line.item1,SymbolItem) or isinstance(line.item1,TempVar):
                        out_put_block.append('          MOV     AX,[DI-'+str(self.off_dic[line.item1.name])+']'+';'+str(line.item1.name))
                    else:
                        out_put_block.append('          MOV     AX,'+str(line.item1))    
                    if isinstance(line.item2,SymbolItem)or isinstance(line.item2,TempVar):
                        out_put_block.append('          MOV     BX,[DI-'+str(self.off_dic[line.item2.name])+']'+';'+str(line.item2.name))
                    else:
                        out_put_block.append('          MOV     BX,'+str(line.item2))    
                    if line.opt in ['+','-']:
                        if line.opt=='+':
                            out_put_block.append('          ADD   AX,BX')
                        else:
                            out_put_block.append('          SUB   AX,BX')
                    elif line.opt in ['*','/']:
                        if line.opt == '*':
                            out_put_block.append('          MUL   BX')
                        else:
                            out_put_block.append('          DIV   BX')
                #要操作的res的偏移地址            
                off_set=0
                tag=1
                if line.res.name in self.off_dic:
                    off_set=self.off_dic[line.res.name]
                else:
                    self.off_dic[line.res.name]=off_set
                    self.control('+',2)
                    tag=0
                    if isinstance(line.res,TempVar):
                        self.Temp_count+=2

                if line.opt=='=':
                    #x=a或者x=2
                    #在表中  
                    if isinstance(line.item1,SymbolItem)or isinstance(line.item1,TempVar):
                        out_put_block.append('          MOV  DX,[DI-'+str(self.off_dic[line.item1.name])+']'+';'+str(line.item1.name))
                    else:
                        out_put_block.append('          MOV    DX,'+str(line.item1))
                out_put_block.append('          MOV     [DI],DX'+';'+str(line.res.name))
                if tag == 0:         
                    out_put_block.append('          ADD    DI,2') 
                    tag=1       
                   

            #转移指令 JMP
            if line.opt in ['>=','<=','==','>','<']:
                logic_op=line.opt
                if isinstance(line.item1,SymbolItem) or isinstance(line.item1,TempVar):
                    out_put_block.append('          MOV     AX,[DI-'+str(self.off_dic[line.item1.name])+']'+';'+str(line.item1.name))
                else:
                    out_put_block.append('          MOV     AX,'+str(line.item1))    
                if isinstance(line.item2,SymbolItem)or isinstance(line.item2,TempVar):
                    out_put_block.append('          MOV     BX,[DI-'+str(self.off_dic[line.item2.name])+']'+';'+str(line.item2.name))
                else:
                    out_put_block.append('          MOV     BX,'+str(line.item2))

                out_put_block.append('          CMP     AX,BX')    
                if 'while' in load_name:
                    '''
                    '''
                    #self.jmp_jud(logic_op,out_put_block,line)
                    #if -else  都有的情况
                    out_put_block.append('          SUB     DI'+str(self.Temp_count))
                    self.control('-',self.Temp_count)
                    self.Temp_count=0
                    if logic_op == '>':
                        out_put_block.append('       JBE  '+self.rea_dic[load_name])

                    if logic_op =='>=':
                        out_put_block.append('       JB  '+self.rea_dic[load_name])
                    
                    if logic_op =='<=':
                        out_put_block.append('       JA  '+self.rea_dic[load_name])

                    if logic_op =='<':
                        out_put_block.append('      JAE  '+self.rea_dic[load_name]) 

                    if logic_op =='==':
                        out_put_block.append('      JNE  '+self.rea_dic[load_name])      
                    pass
                if 'do' in load_name:
                   pass

                if 'we' in load_name:
                    '''
                    '''
                    #print(self.rea_dic[load_name])
                    pass
                
            #包含转移的指令,语句块的出口 
            if line.opt in ['if','el','ie','do','we','wh']:
                if line.opt=='wh':
                    self.while_c+=1
                    name='while'+str(self.while_c)
                    self.while_stack.append(name)
                    self.jm_status[name]='begin'
                    self.rea_dic['do'+str(self.while_c)]='we'+str(self.while_c)
                    self.rea_dic[name]='we'+str(self.while_c)
                    self.rea_dic['we'+str(self.while_c)]=name
                    self.block_name=name
                #do,we 要寻找与之对应的whil，从while栈中栈顶得到    
                if line.opt =='do':
                    name='do'+self.while_stack[-1][5:]
                    self.block_name=name
                if line.opt == 'we':
                    name='we'+self.while_stack[-1][5:]
                    pop_name=self.while_stack.pop()
                     
                    self.block_name=name
                if line.opt=='if':
                    self.if_c+=1
                    name='if'+str(self.if_c)
                    self.if_stack.append(name)
                    self.jm_status[name]='begin'
                    self.rea_dic['else'+str(self.if_c)]='ie'+str(self.if_c)
                    str_v='else'+str(self.if_c)
                    str_c='ie'+str(self.if_c)
                    lis_v=[str_c,str_v]
                    self.rea_dic[name]=lis_v
                    self.rea_dic['ie'+str(self.if_c)]=name
                    self.block_name=name
                    #if 前必定有判断语句
                    out_put_block.append('          SUB     DI'+str(self.Temp_count))
                    self.control('-',self.Temp_count)
                    self.Temp_count=0
                    if logic_op == '>':
                        out_put_block.append('      JBE  '+self.rea_dic[name][-1])

                    if logic_op =='>=':
                        out_put_block.append('       JB  '+self.rea_dic[name][-1])
                    
                    if logic_op =='<=':
                        out_put_block.append('       JA  '+self.rea_dic[name][-1])

                    if logic_op =='<':
                        out_put_block.append('       JAE  '+self.rea_dic[name][-1]) 

                    if logic_op =='==':
                        out_put_block.append('       JNE  '+self.rea_dic[name][-1])

     
                #do,we 要寻找与之对应的whil，从while栈中栈顶得到    
                if line.opt =='el':
                    name='else'+self.if_stack[-1][2:]
                    if_status='if'+name[4:]
                    self.jm_status[if_status]='done'
                    self.block_name=name
                    out_put_block.append('          SUB     DI'+str(self.Temp_count))
                    self.control('-',self.Temp_count)
                    self.Temp_count=0
                    out_put_block.append('          JMP '+self.rea_dic[self.rea_dic[self.rea_dic[name]]][0])
                if line.opt == 'ie':
                    
                    name='ie'+self.if_stack[-1][2:]
                    if len(self.if_stack)==1:
                        self.if_stack.clear()
                    else:
                        pop_name=self.if_stack.pop()                
                    self.block_name=name

            if line.opt == 'ret':
                if isinstance(line.item1,SymbolItem) or isinstance(line.item1,TempVar):
                    #out_put_block.append('          MOV     DX,[DI-'+str(self.off_dic[line.item1.name]+'];'+line.item1.name))
                    out_put_block.append('          MOV  CX,[DI-'+str(self.off_dic[line.item1.name])+']')
                else:
                    out_put_block.append('          MOV     CX,'+str(line.item1))
                out_put_block.append('          SUB     DI;'+str(self.Temp_count))
                self.control('-',self.Temp_count)
                self.Temp_count=0        
                out_put_block.append('  ret')        

        self.out_put=out_put_block
        for i in self.out_put:
            print(i)

        #self.out_put+=out_put_block   
        pass



    #分析语句块
    def parse_main(self):

        #基本块 
        
        print('{}      PROC    NEAR'.format(self.fname.upper()))
        if len(self.f_dict['param'])!=0:
            self.param_perpare()
        self.cut_block()
        print('{}       ENDP'.format(self.fname.upper()))        
        pass

    #函数带参数，要准备
    def param_perpare(self):
        out_put_lis=[]
        out_put_lis.append('          PUSH  BP')
        out_put_lis.append('          MOV   BP,SP')
        #将栈中参数保存
        par_lis=self.f_dict['param']
        base=2
        len_par=len(par_lis)
        for item in par_lis:
            self.off_dic[item]=0
            out_put_lis.append('          MOV   DX,[BP+'+str(base+2*len_par)+']')
            out_put_lis.append('          MOV   [DI],DX')
            out_put_lis.append('          ADD   DI,2')
            self.control('+',2)
            len_par-=1
        for i in out_put_lis:
            print(i)    
        pass

    
    #划分基本块
    def cut_block(self):
        """ for item in self.Qt_lis:
            print(item)
            print('a') """
        lis_block=[]
        for item in self.Qt_lis:
            if isinstance(item,MiddleCode):
                lis_block.append(item)
            else:
                self.parse_block(lis_block)
                pass
                lis_block.clear()

        if len(lis_block)!=0:           
            lis_block.append('')
            self.parse_block(lis_block)
            lis_block.clear()

                    




class Target_cult():
    
    #总 四元式块
    Qt_lis=[]

    def __init__(self):
        self.open_file()
        
        self.clut()

    def open_file(self):
        lis=[]
        o=Optimizer()
        lis=o.get_result()
        self.Qt_lis=lis
    
    def clut(self):
        fun_name=''
        fun_dic=dict()

        #每一块函数的四元式语句块
        fun_lis=[]
        tag=0
        for line in self.Qt_lis:
            #遇到函数dingyi
            
            try:
                if line.opt == 'pro':
                    fun_dic['name']=line.item1.name
                    fun_dic['param']=list()
                    for item in line.item1.addr.paramList:
                        fun_dic['param'].append(item.name)
                    print(fun_dic)
                    tag=1
                    continue
                if line.opt == 'pe':
                    fun_lis.append('')
                    parse=Target_fun(fun_lis[1:],fun_dic)
                    print('1ci')
                    fun_lis.clear()
                    fun_dic.clear()
                    tag=0
                    continue
            except:
                pass        
            if tag == 1:
                fun_lis.append(line)


        print('hello,evevy')
            

if __name__ == '__main__':


    tr=Target_cult()
    print('jel')
    print(('he'))

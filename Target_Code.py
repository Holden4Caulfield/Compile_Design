class Target():

    j_w=['_','+','*','/','=']
    id_list=[]
    lan_block=[]
    Qt_lis=[
        ['=','3','_','a'],
        ['=','2','_','b'],
        ['+','a','b','t1'],
        ['*','a','t1','t3'],
        ['/','t3','t1','x'],
        ['=','t1','_','i']
    ]
    def __init__(self):
        self.get_list()
        self.prepare()
        self.parse_main()
        pass

    def prepare(self):
        print('DSEG     SEGMENT')
        for item in self.id_list:
            print(item['name']+'     '+'DW    '+'?')
        print('DSEG     ENDS')
        print('CSEG     SEGMENT')
        print('    ASSUME CS:CSEG,DS:DSEG')    

    #解析语句块
    def parse_block(self):
        out_put=[]
        for line in self.Qt_lis:
            if line[0] in ['+','-']:
                if line[0]=='+':
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        ADD   AX,'+str(line[2]))
                    out_put.append('        MOV   '+str(line[3])+','+'AX')
                else:
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        SUB   AX,'+str(line[2]))
                    out_put.append('        MOV   '+str(line[3])+','+'AX')
            if line[0] in ['*','/']:
                if line[0] == '*':
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        MUL   '+str(line[2]))
                    out_put.append('        MOV   '+str(line[3])+','+'AX')
                else:
                    out_put.append('        MOV   AX,'+str(line[1]))
                    out_put.append('        DIV   '+str(line[2]))
                    out_put.append('        MOV   '+str(line[3]).upper()+','+'AX')
            if line[0]=='=':

                out_put.append('        MOV   '+'DX'+','+str(line[1]))
                out_put.append('        MOV   '+str(line[3])+','+'DX')    


        for i in out_put:
            print(i)
        pass

    #划分基本块,获得变量表
    def get_list(self):
        #传入四元式,逐条分析
        for items in self.Qt_lis:
            for item in items:
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
        """ kw=['if','ie','el','wh','do','we']
        block=[]
        count=0
        for lis in Qt_lis:
            block.append(lis)
            if lis[0] in kw:
                count+=1
                self.lan_block.append(block)
                block.clear() """
        #基本块 
        print('START: MOV  AX,DSEG')
        print('     MOV  DS,AX')       
        self.parse_block()
        print('CSEG     ENDS')
        print('     END  START')       
                
                
                

        pass


if __name__ =='__main__':
    tr=Target()
    print('dong')
from re import findall, DOTALL
from stUtil import rndrCode
from streamlit import sidebar, columns as stCLMN, radio as stRadio
from os.path import splitext
def 取出片段():
  左, 右=stCLMN([1, 1])
  #宗教商城=['宗教商城I.md', '宗教商城II.md']
  宗教商城=['宗教商城I.md', '宗教商城II.md', '宗教商城III.md', '宗教商城IV.md', '宗教商城V.md', '宗教商城VI.md', '宗教商城VII.md', '宗教商城VIII.md', '宗教商城9.md']
  with sidebar:
    宗教=stRadio('宗教商城', 宗教商城, horizontal=True, index=0)
  if 宗教:
    with 左:
      with open(宗教) as fin:
        base, ext=splitext(宗教)
        fout=open(f'{base}.py', 'w')
        資訊=fin.read()
        得出=findall(r'```python\n(.*?)\n```|```sql\n(.*?)\n```', 資訊, DOTALL)
        rndrCode(['長度', len(得出)])
        #rndrCode([得出])
        for ndx, 片段 in enumerate(得出):
          py片, sql片=片段
          if py片:
            fout.write(py片+'\n')
            rndrCode(py片)
          else:
            fout.write(sql片+'\n')
            rndrCode(sql片)
      fout.close()
    with 右:
      rndrCode(資訊)

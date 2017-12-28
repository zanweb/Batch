# Batch
## 1. Purpose
### 1.1 Effective

|col1|col2|col3|
|---|---|---|
|row|row|row|
|pp|rr|ss|

> block
> block
> block



``` mermaid
graph TD:
    start-->end;
```

``` flow
st=>start: 开始
op_link=>operation: 链接数据库
op_stvar=>operation: setup: starck=1, seq =1
op_read_dict=>operation: Read content as a dict
cond_txt_end=>condition: end of content?
op_read_one_part=>operation: read one part
cond_total_flange_weight=>condition: weight of flanges > 3 tons?
op_stack_add=>operation: stack +=1
op_seq_add=>operation: seq += 1
e=>end: finish
st->op_link->op_stvar->op_read_dict->cond_txt_end->op_read_one_part
cond_txt_end(yes)->e
cond_txt_end(no)->op_read_one_part->cond_total_flange_weight
cond_total_flange_weight(yes)->op_stack_add->op_seq_add
cond_total_flange_weight(no)->op_seq_add->cond_txt_end
```
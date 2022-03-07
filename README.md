# code helper

Author: Kermit Chen

Doc rev: 001





## What this?

- Coding a python script in other code file. e.g.:

  - verilog file
  - VHDL file
  - markdown file
  - text file

- Faster generate code with template or look-up table

- Repeat some operation by python

- Call python script and file that you want to auto generate

  - `python main.py <your_file>`

  



## Render snippet flow

1. Parse all python script block
2. Generate a `_temp.py` with script
3. Find the insert block in your file
4. Insert the snippet by python return dictionary



**NOTICE:**

- Python script first function is `get_dict()`
- **Return must be a dictionary**
  - key: snippet name
  - value: insert snippet
- Insert block is match the name with **dictionary key** when render the code



## Symbol

### Python script block

start symbol default: `//[::pys::]`

end symbol default: `//[::pye::]`

**Recommend: write script block in comment, don't let the python code effect your code**

#### For example

```
//[::pys::]
<your python script>
//[::pye::]
```



### Insert block

start symbol default: `//[::pds::]`

end symbol default: `//[::pde::]`

Call start symbol with snippet name, auto generate code in there after python run.

**Ignore internal block text and update by snippet**



#### For example

```
//[::pys::] <render_dict_name>
**DON'T MODIFY HERE!!**
**Run script will be regenerated every time.**
//[::pye::]
```





## Example code

```
//[::pys::]
def get_dict():
    reDict = {}
    
    reDict['snipA'] = funcA()
    reDict['snipB'] = funcB()
    
    t = ''
    for i in range(10):
    	t += str(i)
    reDict['snipC'] = t

    return reDict
//[::pye::]


...

//[::pds::] snipC

//[::pde::]
```

after run python to render

```
//[::pds::] snipC
0123456789
//[::pde::]
```



# Release notes

Change tags:

- [A] add
- [M] modify
- [RM] remove
- [U] update
- [O] optimize



## 0.0.0

Date: 2022.03.04

Changes:

- [A] Basic function

Fix bugs:

- NA


import jinja2
import re
import enum
import sys
import runpy

ENUM__SNIPPET_TYPE = enum.Enum('ENUM__SNIPPET_TYPE', 'SNIPPET INSERT')

SYMBOL__PY_SNIPPET_START = '//[::pys::]'
SYMBOL__PY_SNIPPET_END = '//[::pye::]'
SYMBOL__PY_DICT_START = '//[::pds::]'
SYMBOL__PY_DICT_END = '//[::pde::]'
SYMBOL__PROTECT = '//#::#:'

SNIPPET_TYPE = {}
SNIPPET_TYPE[SYMBOL__PY_DICT_END] = ENUM__SNIPPET_TYPE.INSERT
SNIPPET_TYPE[SYMBOL__PY_SNIPPET_START] = ENUM__SNIPPET_TYPE.SNIPPET

TEMP_PY_SCRIPT_FILE_NAME = '_tmp.py'
PY_SCRIPT_RUN_FUNC_NAME = 'gen_dict'

RENDER_FILE_PATH = ''

# DEBUG_POINT = 999
    
class Snippet(object):
    def __init__(self, *args):
        self.snipName = ''
        self.snippet_text = ''
        self.token_start = ''
        self.token_end = ''
        self.inside_blk = ''
        self.outside_blk = ''
        self.type_enum = None
        self.render_text = ''


class CodeHelper(object):
    def __init__(self, *args):
        # super(CodeHelper, self).__init__(*args))

        self.CODE_REMOVE_SYMBOL = ''

        self.pySnip_lt = [] #type: list[Snippet]
        self.insertSnip_lt = [] #type: list[Snippet]

        self.main()

    def getPyScript(self):
        ''' Find symbol and split it  '''
        sp_lt = self.REND_SRC_CODE.split(SYMBOL__PY_SNIPPET_START)
        for groupCode in sp_lt[1:]:
            snipSplitByEnd_lt = groupCode.split(SYMBOL__PY_SNIPPET_END)

            if (len(snipSplitByEnd_lt)>1):
                tmp_snip = Snippet()
                tmp_snip.token_start = SYMBOL__PY_SNIPPET_START
                tmp_snip.token_end = SYMBOL__PY_SNIPPET_END
                tmp_snip.snippet_text = snipSplitByEnd_lt[0]
                tmp_snip.type_enum = SNIPPET_TYPE[SYMBOL__PY_SNIPPET_START]
                self.pySnip_lt.append (tmp_snip)
            else:
                print("Error: parse pysnippet")
        
    
    def genTempPyScript(self):
        text = ''
        for pySnip in self.pySnip_lt:
            text += pySnip.snippet_text

            fp = open(TEMP_PY_SCRIPT_FILE_NAME,'w+')
            with fp:
                fp.seek(0)
                fp.write(text)
                fp.close()

    def runScript(self):
        pyScriptRun = runpy.run_path(path_name=TEMP_PY_SCRIPT_FILE_NAME)
        render_dict = pyScriptRun[PY_SCRIPT_RUN_FUNC_NAME]()
        if (
            (render_dict != None)
        ):
            self.render_dict = render_dict
        else:
            print("Error: render_dict == None")
    
    def renderToCode(self):
        sp_lt = self.REND_SRC_CODE.split(SYMBOL__PY_DICT_START)
        self.render_pass = True

        for idx,groupCode in enumerate(sp_lt[1:]):
            idx += 1
            snipSplitByEnd_lt = groupCode.split(SYMBOL__PY_DICT_END)

            rePtn = '%s (.+)'%(re.escape(SYMBOL__PY_DICT_START))
            tmp_str = SYMBOL__PY_DICT_START + snipSplitByEnd_lt[0]
            reRes = re.findall(rePtn,tmp_str)
            dictName = reRes[0]

            ''' Find snippet by dictName'''
            dict_res = ''
            try:
                dict_res = str(self.render_dict[dictName])
            except:
                print("[Error] dictName not found: %s"%(dictName))
                self.render_pass = False

            if (self.render_pass):
                if (len(snipSplitByEnd_lt)>1):
                    remainSnip = snipSplitByEnd_lt[1]
                else:
                    ''' Non end symbol mode '''
                    remainSnip = ''
                
                tmp_str = '%s %s\n'%(
                    SYMBOL__PY_DICT_START
                    ,dictName
                )
                tmp_str += dict_res + '\n' + SYMBOL__PY_DICT_END + remainSnip

                sp_lt[idx] = tmp_str

        render_all_text = ''
        if (self.render_pass):
            for render_text in sp_lt:
                render_all_text += render_text
            print(render_all_text)
            
            self.render_all_text = render_all_text
        return render_all_text

    def main(self):
        # RENDER_FILE_PATH = 'test.v'
        rendFile = open(RENDER_FILE_PATH,'r+')
        with rendFile:
            # print (rendFile.read())
            rendFile.seek(0)
            self.REND_SRC_CODE = rendFile.read()
            self.REND_SRC_CODE_ORG = self.REND_SRC_CODE
            rendFile.close()

            self.getPyScript()
            self.genTempPyScript()

            self.runScript()

            self.renderToCode()
            
            if (self.render_pass):
                bakFile = open(RENDER_FILE_PATH+'.bak','w+')
                with bakFile:
                    bakFile.seek(0)
                    bakFile.write(self.REND_SRC_CODE_ORG)

                rendFile = open(RENDER_FILE_PATH,'w+')
                with rendFile:
                    rendFile.seek(0)
                    rendFile.write(self.render_all_text)


if __name__ == '__main__':
    arg_error = False
    try:
        RENDER_FILE_PATH = sys.argv[1]
    except:
        print('File path error')
        arg_error = True
    
    if (arg_error == False):
        cg = CodeHelper ()
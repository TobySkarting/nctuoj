import os
import subprocess as sp

class Sandbox:
    class SandboxOption:
        def __init__(self):
            meta = {}
            meta['dir'] = {'/var': None}
            meta['env'] = {'PATH': '$PATH:/usr/lib/jvm/java-7-openjdk-amd64/bin/:/usr/lib/ghc'} 
            meta["cgroup"] = True               #--cg
            meta["full_env"] = True             #--full-env
            meta["input"] = ''                  #--stdin
            meta["output"] = ''                 #--stdout
            meta["errput"] = ''                 #--stderr
            meta["meta"] = ''                   #--meta
            meta["mem_limit"] = 65535           #--mem
            meta['proc_limit'] = 1              #--processes
            meta['time_limit'] = 1              #--time
            meta['fsize_limit'] = 65535         #--fsize
            self._meta = meta

        def set_env(self, **kwargs):
<<<<<<< HEAD
            for var, val in kwargs.items():
                val = '$%s:%s'%(var, val)
            self._meta['env'].update(kwargs)

        def set_dir(self, **kwargs):
            self._meta['dir'].update(kwargs)
=======
            self._meta.update(kwargs)
>>>>>>> bb741647604bbd0bfa762bbb32407418ceefc225

        def set_options(self, **kwargs):
            self._meta.update(kwargs)

        def __getitem__(self, index):
            return self._meta[index]

    def __init__(self, box_id, isolate):
        self._isolate = isolate
        self._box_id = box_id
        self._opt = self.SandboxOption()
        pass

    def set_options(self, **kwargs):
        self._opt.set_options(**kwargs)

    def init_box(self):
        cmd = self._isolate + ' '
        cmd += '--box-id=%s '%(str(self._box_id))
        if self._opt['cgroup']: cmd += '--cg '
        cmd += '--init'
        sp.call(cmd, shell=True)

    def delete_box(self):
        cmd = self._isolate + ' --box-id=%s --cleanup'%(str(self._box_id)) 
        print(cmd)
        sp.call(cmd, shell=True)

    
    def exec_box(self, exec_cmd):
        cmd = self._isolate + ' '
        cmd += '--box-id=%s '%(str(self._box_id))
        if self._opt['full_env']: cmd += '--full-env '
        if self._opt['input']: cmd += '--stdin=%s '%self._opt['input']
        if self._opt['output']: cmd += '--stdout=%s '%self._opt['output']
        if self._opt['errput']: cmd += '--stderr=%s '%self._opt['errput']
        if self._opt['meta']: cmd += '--meta=%s '%self._opt['meta']
        if self._opt['mem_limit']: cmd += '--mem=%s '%(str(self._opt['mem_limit']))
        if self._opt['mem_limit']: cmd += '--cg-mem=%s '%(str(self._opt['mem_limit']))
        if self._opt['proc_limit']: cmd += '--processes=%s '%(str(self._opt['proc_limit']))
        if self._opt['time_limit']: cmd += '--time=%s '%(str(self._opt['time_limit']))
        if self._opt['time_limit']: cmd += '--wall-time=%s '%(str(self._opt['time_limit']*1.3))
        if self._opt['fsize_limit']: cmd += '--fsize=%s '%(str(self._opt['fsize_limit']))
        if self._opt['env']: 
            for (var, val) in self._opt['env'].items():
                cmd += '--env=%s=%s '%(var, val)
        if self._opt['dir']:
            for (out, _in) in self._opt['dir'].items():
                if _in:
                    cmd += '--dir=%s=%s '%(out, _in) 
                else:
                    cmd += '--dir=%s '%(out)
        cmd += '--extra-time=0.2 '
        cmd += '--run -- %s'%exec_cmd
        print("Run: ", exec_cmd)
        #return sp.call(cmd, shell=True, stdout=sp.DEVNULL, stderr=sp.DEVNULL)
        return sp.call(cmd, shell=True)

        
if __name__ == "__main__":
    s = Sandbox(1, './isolate')
<<<<<<< HEAD
    s.set_options(proc_limit=4, meta='meta', mem_limit=65535*20)
=======
    s.set_options(proc_limit=16, meta='meta', errput='err', mem_limit=0, time_limit=3)
>>>>>>> bb741647604bbd0bfa762bbb32407418ceefc225
    s.init_box()
    s.exec_box("/usr/bin/env go")
    #s.delete_box()

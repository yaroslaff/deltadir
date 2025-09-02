# DeltaDir

Compare directories (different methods) and optionally sync it.

## Examples
### Create test environment
~~~bash
# prepare two identical directories
mkdir -p /tmp/src/subdir
echo x > /tmp/src/test.txt
echo x > /tmp/src/subdir/test.txt
cp -a /tmp/src /tmp/dst
~~~

### find missing files
Default mode is `exists` - file considered different if it's completely missing in dst/

~~~bash
# create new file in src
echo new > /tmp/src/new.txt

# new file is found
deltadir /tmp/src/ /tmp/dst/
new.txt

# lets -s / --sync it!
deltadir /tmp/src/ /tmp/dst/ --sync
new.txt
~~~


### find updated file

you can use `-m`/`--method` (exists, mtime, size, hash) for more accurate checking

~~~bash
# create new file in src
echo new content > /tmp/src/new.txt

# find nothing
deltadir /tmp/src/ /tmp/dst/

# use hash (slowest, but most reliable) and detect it
deltadir /tmp/src/ /tmp/dst/ -m hash
new.txt

# sync with overwrite
deltadir /tmp/src/ /tmp/dst/ -m hash -s --overwrite
new.txt
~~~

### always recursive
deltadir always work recursively.

~~~bash
echo new > /tmp/src/subdir/newfile.txt

deltadir /tmp/src/ /tmp/dst/ 
subdir/newfile.txt
~~~

### see result as table
Add `-t`/`--table` to see results as table:
~~~
deltadir /tmp/src/ /tmp/dst/  -t
File                                     | Reason          | Src                  | Dst                  | Action              
-----------------------------------------------------------------------------------------------------------------------------
subdir/newfile.txt                       | missing         | -                    | -                    | nothing(reported)   
~~~

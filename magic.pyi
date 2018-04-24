print(f'load stub {__name__} from {__file__}')
import relativ

print('module', repr(relativ))
for key in dir(relativ):
    if key == '__builtins__':
        print(key)
    else:
        print(f'{key} \t {getattr(relativ, key)}')



def call() -> relativ.VAR: ...

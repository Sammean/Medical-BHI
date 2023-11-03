import os, glob


root = os.path.join(os.getcwd(), 'Paired', 'Reg_with_MNI152')
for i in os.listdir(root):
    img = os.path.join(root, i)
    des = os.path.join(os.path.dirname(root), 'extract_brain', i.split('.')[0])

    cmd = (f'bet {img} {des} -R -m')
    print(cmd)
    os.system(cmd)
    # break



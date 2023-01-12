import streamlit
import math
import itertools
import matplotlib.pyplot as plt
import matplotlib.patches

def cyclic_perm(a):
    n = len(a)
    return [tuple(a[i - j] for i in range(n)) for j in range(n)]

cols = ['r','y','g','b','c','m']

ncols = 5
npieces = 4

ncols = streamlit.number_input("Number of colors:",2,6,4)
npieces = streamlit.number_input('Number of pieces:',2,6,4)

combs = itertools.product(range(ncols),repeat=npieces)

nall = ncols ** npieces
ncolumns = math.ceil(nall**.5)

r0 = 4
w0 = 5
wc = 2 + w0 + 2
w = (ncolumns-1) * wc

fig, ax = plt.subplots()
ax.set_xlim(-wc, w+wc)
ax.set_ylim(-wc, w+wc)
ax.yaxis.set_visible(False)
ax.xaxis.set_visible(False)
ax.set_axis_off()
plt.gca().invert_yaxis()
fig.tight_layout()

dct = []
ct = {}

idx = 0
n = 0
for i in itertools.product(range(ncols),repeat=npieces):

  idx0 = min(dct.index(j) if j in dct else 1e10 for j in cyclic_perm(i) )

  if idx0 < 1e10:
    alp = 0.2
    ct[idx0] += 1
  else:
    alp = 1
    ct[idx] = 1
  dct += [i]

  x = (idx% ncolumns) * wc
  y = (idx//ncolumns) * wc

  for j in range(npieces):
    ax.add_patch(matplotlib.patches.Wedge(center=(x, y),r=r0,theta1=360*j/npieces,theta2=360*(j+1)/npieces, facecolor=cols[i[j]], alpha=alp))

  idx += 1

  if idx0 < 1e10:
    x0 = (idx0% ncolumns) * wc
    y0 = (idx0//ncolumns) * wc
    #ax.plot([x,x0],[y,y0],'k-')
    for txt in ax.texts:
      if txt.get_position() == (x0-r0/2,y0+r0/2):
        txt.remove()
    ax.text(x0-r0/2, y0+r0/2, ct[idx0], fontsize=15)

  # plt.savefig('foo'+str(idx)+'.png')

  # for line in ax.get_lines():
  #   line.remove()
fig
streamlit.write("Number of different pieces:",len(ct))

# import imageio
# images = []
# for i in range(1,257):
#     images.append(imageio.imread('foo'+str(i)+'.png'))
# for i in range(10):
#   images.append(imageio.imread('foo256.png'))
# imageio.mimsave('foo.gif', images)
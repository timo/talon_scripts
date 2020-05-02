from talon import noise

def on_pop(noise):
    print("pop!")
noise.register('pop', on_pop)

def on_hiss(noise):
    print("hiss!", noise)

noise.register('hiss', on_hiss)

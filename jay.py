#
# Can you see this?
# Okay, let's start
#
# We we're talking about functions, weren't we?
# You mentioned function prototypes?
#
# That's a term from C and C++
# Have I ever mentioned prototypes?
# Well, you seemed confused about it
# Anything you'd like to ask?
# 
# Ok, but it's nothing to do with Python, really
# In C and C++, you can declare a function without implementing it
# Back to Python!

# Let's define a function
# Python is not statically typed, which means that the same variable can
# refer to values of different types on differen occasions

# This means that you dont specify the types of the arguments or
# the return value

# An example:
# What shall we call it?

def muppetizer(name):
	# Pass is a placeholder for a code block, btw
	# It doesnt do anything
	print('%s is a stupid lil\' muppet!' % name)

# See what it does?
# Tell me, then?
# Good
# Let's try it out!
# 
# In Python, you don't really need a main() function, but lets create one anyway!


def divider():
	# See how it works?
	print('{0}{1}{0}'.format('\n', '-'*60)) # This adds a divider between the outputs from two sections of code
	# The numbers within the curly braces tells the function which argument to format() should be inserted there
	# So {0} means the first argument and {1} means the second
	# Therefore, '\n' gets inserted at either end of the string
	# There is no P0, as far as I can see
	# There are more advanced formatting options, but that's for another time


def main():
	# I've made it a bit more advanced by including a loop
	# What do these lines do?
	# Yes, very good
	# Let's run it!
	for muppet in ['Swift', 'Jon', 'Jay', 'Brandon', 'Little Pretend Aussie Gangster']:
		muppetizer(muppet)

	divider()

	print('%.2f' % 0.22222)
	print('%.2f' % 0.22522)

	divider()

	# What next? How about varargs?
	# Do you remember that we sometimes write arguments like this:
	# In a function definition, they serve as default values for arguments
	# That way, you don't have to specify every option if you don't want to
	# Just rely on the default behaviour
	# For instance, most people probably want coffee for breakfast, but some people prefer tea
	# Let's be helpful to the former by making coffee the default
	# As you can see, you can make some arguments non-optional
	def haveBreakfast(bread, drink='coffee', location='Kitchen Sofa'):
		print('Yummy! %s tastes so good with %s!' % (bread, drink))
	# Did you see how we just defined a function inside a function?
	# This is perfectly ok in Python: you can define functions on the fly!
	# You want have access to out outside of this function, because of namespaces
	# Yes, it is very good that you remember scope and namespaces
	# You can actually get all variables defined in the correct context like so:
	# Let me show you namespaces in action

	return haveBreakfast

# Let's move on to another aspect of functions, ok?
# In Python, there is such a thing as varargs and kwargs
# or variable arguments and keyword arguments
# Functions which allow such parameters are declared like so:

# doSomeCoolStuff is a function that accepts any number of positional (*varargs) and keyword arguments (**kwargs)
# You can call the arguments anything you like; it is the asterisks that make them special, not the name. Got it?
# This is used in the built-in print function

# What do you think this does?
# Yes, separated by a space (sorry)
# Print DOES add a newline afterwards, though
# You can change separators optionally with a keyword argument:


# Inside a function definition, *args is available as a tuple and **kwargs is available as a dictionary
def doSomeCoolStuff(*varargs, **kwargs):
	# What do you think this does?
	# Prints what?
	print('KEY | VALUE')
	for key, value in kwargs.items():
		print('%s | %s' % (key, value))


if __name__ == '__main__':
	breakfast = main()
	breakfast('baguette', location='My room')

	divider()

	doSomeCoolStuff('cat', 'dog', 'mouse', horse='neigh', dog='bark', cat='miau') # Anyway, what will this do?
	# No, but almost
	# No, I want you to think about it
	# Look at the function definition

	divider()
	
	# There's one more thing I should mention

	#If you have a list or tuple (or whatever) of items which you'd like to pass to a function taking *varags, you can do it like so:
	# See the * in front of the list? This is basically like unpacking the list into separate arguments. Got it?
	# You can do the same with dictionaries (and objects supporting the same interface) like so
	doSomeCoolStuff(*['cat', 'dog', 'hyena', 'ocelot', 'macaw', 'platypus', 'dog turd'], **{'horse': 'neigh', 'dog': 'bark', 'cat': 'miau', 'platypus': 'spoilspurt'})


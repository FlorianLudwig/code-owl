code-owl
========

State
-----
This is a proof of concept.  There is a lot to improve.  This is a quick demo so I can show it to others and get some discussion started.  You can install it via `pip install codeowl`.
Code search is python only. Support for other languages is postponed.

What?
-----

It is a new (to my knowledge) way to search source code.

Why?
----
Searching within code relies mostly on string matching or on regular expressions.

I like to suggest that there are better "DSL"s than regular expressions to search code: Using Python syntax to search Python.


Example
-------
The following example is for searching Python source code but the search algorithm would work just as well on a wide arrange of languages. Inside the code are currently literally three lines of python specific tweaking.


Given the following source code:

```python

def foo():
    print 'hello_world'
    hello_world = 1  # useless comment about hello_world being increased


def hello_world():
    print 'world'
    print 'this is inside def hello_world'
```


I hope nobody's short term memory forces them to actually search such small code but for this example we pretend we want to search within it.

Lets say you are looking for the definition of the function `hello_world`. You type `def hello_world`:

![search def hello_world](https://raw.githubusercontent.com/FlorianLudwig/code-owl/master/doc/search_1.png)


Ok, no magic here, we find what we are looking for.  Actually most IDEs do provide a way to search for functions.  But did you notice how it did find the function declaration but did ignore the "def hello_world" part within the print two lines further down?

Now what if you really want to search for a `hello_world` within a string? You don't care about the pointless variable, the useless comment nor the function - just the real thing: the string that gets printed.

![search "hello_world"](https://raw.githubusercontent.com/FlorianLudwig/code-owl/master/doc/search_2.png)

(Yeah, the match highlighting needs some work)

Well, you specify a string if you search a string. Note that there is exactly no difference between `'hello_world'` and `"hello_world"` as query.  After all those are the exact same thing in Python.  Now lets look for `world`:

![search "world"](https://raw.githubusercontent.com/FlorianLudwig/code-owl/master/doc/search_3.png)

So much today is about relevance why are most code searches sorted in order of occurrence?  So for sure the exact match comes first.  And here the last two missing examples:


![search # hello_world](https://raw.githubusercontent.com/FlorianLudwig/code-owl/master/doc/search_4.png)

![search hello_world](https://raw.githubusercontent.com/FlorianLudwig/code-owl/master/doc/search_5.png)


How?
----
The first approach was matching tokens generated from [pygemnts](http://pygments.org/). Which works remarkable well.
But to support a little more semantics I am going for AST-based matching. This does bloat the simple code and I loose
the language neutrality I had but it provides solution for the corner cases that actually matter.

TODO
----

 * recognize blocks and utilize them in search
 * Support for non-python searches
 * speed improvements
 * write a plugin for my IDE of choice
 * improve cli
 * Fix match highlighting
 * For search improvements, [test/todo.py](https://github.com/FlorianLudwig/code-owl/blob/master/test/todo.py)

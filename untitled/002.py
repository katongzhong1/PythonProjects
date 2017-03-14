# !/usr/bin/env python
# coding:utf-8

__metaclass__ = type


class Person:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def color(self, color):
        print "%s is %s" % (self.name, color)

if __name__ == "__main__":
    girl = Person('katongzhong')
    print girl.name
# **MEMOIZATION EXERCISE**

#### **DESCRIPTION:**
This project's aim is to create a function / method that is able to memoize results of a specific function, return and keep them for as long as their life-span does not exceed the defined timeout and consistently test it out.

#### **REQUIRED DEPENDENCIES:**
- FreezeGun


### **TEST SUMMARY:**

#### **VERIFIED FUNCTIONALITY:**
- [x] The resolver is used as cache key
- [x] The result of the passed function is memorized
- [x] The values are correctly returned depending on the resolver
- [x] After the timeout expires the values are deleted

#### **DATA TYPE TESTING:**
###### **RESULT WITHOUT PROVIDED FUNCTION (addToTime):**
- string: failure
- integer: successfuly memoized
- float: successfuly memoized
- complex: successfuly memoized
- list: failure
- tuple: successfuly memoized
- range: successfuly memoized
- dictionary: failure
- set: failure
- frozen set: successfuly memoized
- boolean: successfuly memoized
- bytes: successfuly memoized
- bytearray: failure
- memory view: successfuly memoized

###### **RESULT WITH IMPLEMENTATION OF THE PROVIDED FUNCTION (addToTime):**
- string: failure
- integer: successfuly memoized
- float: successfuly memoized
- complex: failure
- list: failure
- tuple: failure
- range: failure
- dictionary: failure
- set: failure
- frozen set: failure
- boolean: successfuly memoized
- bytes: failure
- bytearray: failure
- memory view: failure

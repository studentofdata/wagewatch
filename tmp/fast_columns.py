
For the first part you can pass a dict of column names for keys and a list of functions for the values:

In [28]: df
Out[28]:
          A         B         C         D         E  GRP
0  0.395670  0.219560  0.600644  0.613445  0.242893    0
1  0.323911  0.464584  0.107215  0.204072  0.927325    0
2  0.321358  0.076037  0.166946  0.439661  0.914612    1
3  0.133466  0.447946  0.014815  0.130781  0.268290    1

In [26]: f = {'A':['sum','mean'], 'B':['prod']}

In [27]: df.groupby('GRP').agg(f)
Out[27]:
            A                   B
          sum      mean      prod
GRP
0    0.719580  0.359790  0.102004
1    0.454824  0.227412  0.034060
UPDATE 1:

Because the aggregate function works on Series, references to the other column names are lost. To get around this, you can reference the full dataframe and index it using the group indices within the lambda function.

Here's a hacky workaround:

In [67]: f = {'A':['sum','mean'], 'B':['prod'], 'D': lambda g: df.ix[g.index].E.sum()}

In [69]: df.groupby('GRP').agg(f)
Out[69]:
            A                   B         D
          sum      mean      prod  <lambda>
GRP
0    0.719580  0.359790  0.102004  1.170219
1    0.454824  0.227412  0.034060  1.182901
Here, the resultant 'D' column is made up of the summed 'E' values.

UPDATE 2:

Here's a method that I think will do everything you ask. First make a custom lambda function. Below, g references the group. When aggregating, g will be a Series. Passing g.index to df.ix[] selects the current group from df. I then test if column C is less than 0.5. The returned boolean series is passed to g[] which selects only those rows meeting the criteria.

In [95]: cust = lambda g: g[df.ix[g.index]['C'] < 0.5].sum()

In [96]: f = {'A':['sum','mean'], 'B':['prod'], 'D': {'my name': cust}}

In [97]: df.groupby('GRP').agg(f)
Out[97]:
            A                   B         D
          sum      mean      prod   my name
GRP
0    0.719580  0.359790  0.102004  0.204072
1    0.454824  0.227412  0.034060  0.570441
from tomd import Tomd

table='''
<table>
    <thead>
        <tr>
            <th>head1</th>
            <th>head2</th>
            <th>head3</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>content1</td>
            <td>content2</td>
            <td>content3</td>
        </tr>
    </tbody>
</table>
'''


md = Tomd(table).markdown
print("~~~~~~~~~~~~~")
print(md)
print("~~~~~~~~~~~~~")

'''
output
|head1|head2|head3
|------
|content1|content2|content3|
'''


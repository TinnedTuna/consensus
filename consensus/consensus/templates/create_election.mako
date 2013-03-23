<%inherit file='base.mako'/>
<div id='create-election-form'>
  <form action='${create_url}' method='POST'>
    <label for='election_name'>Election Name</label>
    <input type='text' name='election_name' />
    <label for='election_body'>Election Body</label>
    <input type='textarea' name='election_body' />
    <label for='methods'>Choose an election method:</label>
    <select name='methods'>
    % for method in methods:
      <option value='${method.python_name}'>${method.name}</option>
    % endfor
    </select>
    <input type='submit' value='Create' />
  </form>
</div>
      
      

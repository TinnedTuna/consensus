<%inherit file='base.mako'/>

  <div id='signin'>
    <form action='${submit_url}' method='POST'>
      <input type='text' name='username'/>
      <input type='password' name='password'/>
      <input type='submit' name='submit' value='Submit'/>
    </form>
  </div>
  

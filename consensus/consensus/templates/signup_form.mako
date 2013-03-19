<%inherit file='base.mako'/>
  <form action='${submit_url}' method='POST'>
    <input type='text' name='username'/>
    <input type='password' name='password'/>
    <input type='submit'/>
  </form>

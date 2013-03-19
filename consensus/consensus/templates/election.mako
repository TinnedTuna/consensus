<%inherit file='base.mako'>

  <div id='election_details'>
    <h2>${election['name']}</h2>
    <div id='election_body'>
      ${election['body']}
    <%page args=election['method']>
    </div>
  </div>
    

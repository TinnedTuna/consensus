<%inherit file='base.mako'/>

<h2>All Elections</h2>
  <div class='elections'>
  #% for election in ${elections}
    <div class='election'>
      ${elections}
    </div>
  #% endfor
  </div>


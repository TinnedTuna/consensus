<div id='ballot'>
  <form>
  % for element in ballot_config['required']:
    % if element.label is not none:
      <label>*${element['label']}</label>
    % else:
      *
    % endif
    <${element['html_type'] type="${element['type']}" name="${element['name'}" value="${element['value']" />
  % endfor
  % for element in ballot_config['required']:
    % if element.label is not none:
      <label>${element['label']}</label>
    % endif
    <${element['html_type'] type="${element['type']}" name="${element['name'}" value="${element['value']" />
  % endfor
  </form>
</div>

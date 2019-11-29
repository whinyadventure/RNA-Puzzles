// prevent menus ovelapping in mobile ver

$('#links').on('show.bs.collapse', function () {
  $('#account').collapse("hide");
})

$('#account').on('show.bs.collapse', function () {
  $('#links').collapse("hide");
})
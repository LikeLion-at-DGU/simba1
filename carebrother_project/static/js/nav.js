const dropdownTrigger = document.querySelector('.dropdown_click');

dropdownTrigger.addEventListener('click', function() {
  const dropdownMenu = document.querySelector('.navbar li ul');
  if (dropdownMenu.style.display === 'block') {
    dropdownMenu.style.display = 'none'; // 드롭다운 메뉴가 보이는 상태일 경우 숨김 처리
  } else {
    dropdownMenu.style.display = 'block'; // 드롭다운 메뉴가 숨겨진 상태일 경우 표시
  }
});

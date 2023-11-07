const allSdeMenu = document.querySelectorAll('#sidebar .side-menu li a');

allSdeMenu.forEach(item=> {
    const li = item.parentElement;

    item.addEventListener('click', function () {
        allSdeMenu.forEach(i=> {
            i.parentElement.classList.remove('active')
        })
        li.classList.add('active');
    })
});

//TOGGLE SIDEBAR

const menuBar = document.querySelector('.fa-bars');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
    sidebar.classList.toggle("hide"); 
});



const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .fa-solid');
const searchForm = document.querySelector('#content nav form');

    searchButton.addEventListener('click', function(e) {
        if(window.innerWidth < 576) {
            e.preventDefault();
            searchForm.classList.toggle('show');
            if(searchForm.classList.contains('show')) {
                searchButtonIcon.classList.replace('fa-magnifying-glass', 'fa-x');
            }else {
                searchButtonIcon.classList.replace('fa-x', 'fa-magnifying-glass', );
            }
        }
  
    })




    if (window.innerWidth < 780) {
        sidebar.classList.add("hide");
    }else if(window.innerWidth > 576){
        searchButtonIcon.classList.replace('fa-x', 'fa-magnifying-glass', );
        searchForm.classList.remove('show');
    }

window.addEventListener('resize', function() {
    if(this.innerWidth > 576){
        searchButtonIcon.classList.replace('fa-x', 'fa-magnifying-glass', );
        searchForm.classList.remove('show');
    }
})
    



document.querySelector("#overview > div:nth-child(2) > div.col-lg-8.d-flex.flex-column > div:nth-child(2) > div > div > div")

var newMemberBtn = document.querySelector('.adMembersBtn');
var darkBg = document.querySelector('.dark_bg');
var popinForm = document.querySelector('.popup');
var closeBtn = document.querySelector('.closeBtn')
var submitBtn = document.querySelector('.submitBtn');
var modalTittle =document.querySelector('.modalTittle');
var popinFooter = document.querySelector('.popinFooter');
var form = document.querySelector('form');
var nameEl = document.getElementById('name');
var phoneEl = document.getElementById('phone');
var startEl = document.getElementById('start_date');
var finishEl = document.getElementById('finish_date');
var phoneIIEl = document.getElementById('phone2');
var plateEl = document.getElementById('plate_no');
var sponsorEl = document.getElementById('text');
var addressEl = document.getElementById('address');
var enteries = document.querySelector('.ShowEntries');
var tabSize =  document.getElementById('table_size');
var userInfo = document.querySelector(".userInfo");
var allinput = form.querySelectorAll("input");










// end global variable here //





//image variable //


//start delete//
var i;
var deleteButtons = document.querySelectorAll(".del-btn");
for (var i = 0; i < deleteButtons.length; i++) {
    deleteButtons[i].addEventListener('click', function(e) {
        e.preventDefault();
        if (confirm('Unataka kufuta dereva huyu?')) {
            var driverId = this.dataset.driverid;
            deleteDriver(driverId);
            console.log('number:', driverId)
        }
    });
}

function deleteDriver(driverId) {
    const url = '/delete_driver'
    fetch(url + '?driverId=' + driverId ,{
        method: 'GET',  
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.deleted) {
            var row = document.querySelector('[data-driverid="' + driverId + '"]').closest('tr');
            row.remove();

        }
    });
}



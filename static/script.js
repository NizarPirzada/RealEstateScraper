/*-----------------------------Variables----------------------------*/
const arrData = [];
// const alert = useAlert()
const Pending = 0;
const Done = 1;
let Pause = 2;
let Resume = 1;
let isWebValid = false;
let isEmailValid = false;
const format = "HH:mm";
//let url = "http://192.168.18.46:5001";
let url = "";

$("#start_time").datetimepicker({
	format: "HH:mm:00"
});

$("#end_time").datetimepicker({
	format: "HH:mm:00"
});

// $('#start_time').timepicker({
//     timeFormat: 'HH:mm:00',
//     interval: 60,
//     dynamic: false,
//     dropdown: true,
//     scrollbar: true
// });

// $('#end_time').timepicker({
//     timeFormat: 'HH:mm:00',
//     interval: 60,
//     dynamic: false,
//     dropdown: true,
//     scrollbar: true,
// 	showSeconds: false
// });

/*--------------------------------Add fields in form--------------------------------*/

$(document).ready(function () {
	var max_fields = 1000; //maximum input boxes allowed
	var wrapper = $(".main_div"); //Fields wrapper
	var add_button = $(".add_btn"); //Add button ID
	var submit_data = $("#submit_data");
	var x = 1; //initlal text box count
	add_button.attr('disabled', true);
	

	$(add_button).click(function (e) {
		//on add input button click
		let next_value = parseInt(add_button.val()) + 1;
	
		add_button.val(String(next_value));
		

		e.preventDefault();
		if (x < max_fields) {
			//max input box allowed
			x++; //text box increment
			$(wrapper).append(
				`<div id="row_${next_value}" class="row" style="margin-top:0.5rem"><div class="col-11"><div class="row webrow"><div class="col-9"><input id="website_${next_value}" placeholder="Enter website" class="form-control web_input" oninput="handleWebsiteTextareaChange()"></input></div><div class="col-3"><input class="form-control desired_input" id="desired_price_${next_value}" type="number" oninput="handlePriceChange()" step="100"></div></div></div><div class="col-1"><button id="remove_website" class="remove_field btn btn-primary" value="1">x</button></div></div>`
			); //add input box
		}
		add_button.attr('disabled', true);
	});

	$(wrapper).on("click", ".remove_field", function (e) {
		//user click on remove text
		$('.add_btn').attr('disabled', false);
		e.preventDefault();
		$(this).parent("div").parent("div").remove();
		x--;
	});
});

/*----------------------Changing Functions--------------------*/

function handleWebsiteTextareaChange() {
	
	document.getElementById("website_1").value;
	var add_button = $(".add_btn"); //Add button ID
	
	if ($('.web_input').val() != '' && $('.desired_input').val() != '') {
		add_button.attr('disabled', false);
	} 
	else if ($('.web_input').val() != '' && $('.desired_input').val() == '') {
		add_button.attr('disabled', true);
	}
	else if ($('.web_input').val() == '' && $('.desired_input').val() != '') {
		add_button.attr('disabled', true);
	}
	else {
		add_button.attr('disabled', true);
	}
}

function handleEmailTextareaChange() {
	document.getElementById("email").value;
}

function setStartDate() {
	document.getElementById("start_time").value;
}

function setEndDate() {
	document.getElementById("end_time").value;
}

function handlePriceChange() {
	document.getElementById("desired_price_1").value;
	var add_button = $(".add_btn"); //Add button ID


	if ($('.web_input').val() != '' && $('.desired_input').val() != '') {
		add_button.attr('disabled', false);
	} 
	else if ($('.web_input').val() != '' && $('.desired_input').val() == '') {
		add_button.attr('disabled', true);
	}
	else if ($('.web_input').val() == '' && $('.desired_input').val() != '') {
		add_button.attr('disabled', true);
	}
	else {
		add_button.attr('disabled', true);
	}
}

function getValueByID(id) {
	return document.getElementById(id).value;
}

function getValueByClass(id) {
	return document.getElementByClassName(id).value;
}

function updateCheckbox() {
	var is_proxy = document.getElementById("is_proxy").value;
	if (is_proxy === "1") {
		document.getElementById("is_proxy").value = "0";
		console.log(is_proxy);
	} else {
		document.getElementById("is_proxy").value = "1";
		console.log(is_proxy);
	}
}

function range(start, end) {
	return Array(end - start + 1)
		.fill()
		.map((_, idx) => start + idx);
}

/*-----------------------------JQuery datatable & Get Data----------------------------*/

/* Formatting function for row details - modify as you need */
function format_child_row(d) {
	// `d` is the original data object for the row
	return (
		"<tr>" +
		"<td>" +
		d.url +
		"</td>" +
		"<td>" +
		d.desired_price +
		"</td>" +
		'<td style="display:none">' +
		d.website_id +
		"</td>" +
		"</tr>"
	);
}

$(document).ready(function () {
	var table = $("#configuration_table").DataTable({
		ajax: {
			url: url + '/configuration/',
			method: "GET",
			xhrFields: {
				withCredentials: true,
			},
			dataSrc: function (data) {
			    return data;
			},
		},
		columns: [
			{
				className: "details-control",
				orderable: false,
				data: null,
				// defaultContent: "+",
				render: function ( data, type, row ) {
					return '<i class="fas fa-angle-down color" aria-hidden="true"></i>';
				  }
			},
			{
				data: "created_date",
				render: function formatDate(value, index) {
                    var date;
					if (!value){
					    value = moment.utc(new Date());
					}
					var todayDate = moment.utc(new Date());
					var todaydateFormat = todayDate.format("yyyy-MM-DD HH:mm:ss");
					var todayDatemom = moment(todaydateFormat);
					var minutes = todayDatemom.diff(value, "minutes");
					if (minutes <= 0) {
						date = "few seconds ago";
					} else if (minutes > 0 && minutes < 60) {
						date = minutes + " minutes ago";
					} else if (minutes > 60 && minutes < 1440) {
						var hours = todayDatemom.diff(value, "hours");
						if (hours == 1) {
							date = hours + " hour ago";
						} else {
							date = hours + " hours ago";
						}
					} else if (minutes > 1440) {
						var days = todayDatemom.diff(value, "days");
						if (days == 1) {
							date = days + " day ago";
						} else {
							date = days + " days ago";
						}
					}
					if (!date){
					    date = '--'
					}
					return date;
				},
			},
			{ data: "emails" },
			{ data: "start_time" },
			{ data: "end_time" },
			{
				data: "is_proxy", render: function (data, type, row) {
					return data == '1' ? '<span class="d-inline-block tip" tabindex="0" data-toggle="tooltip" title="Proxy Enabled"><i class="fa fa-check-square"></i></span>' : '<span class="d-inline-block tip" tabindex="0" data-toggle="tooltip" title="Proxy Disabled"><input class="" type="checkbox" disabled value=""  id="proxy" /></span> '
				}
				
			},
			{ data: "execution_status" },
			{
				data: "active_state", "className": 'active_state', render: function (data, type, row) {
					return data == '1' ? `<span class="d-inline-block tip" tabindex="0" data-toggle="tooltip" title="Active"><i class="fa fa-circle green" aria-hidden="true" value=${data}></i></span>` : `<span class="d-inline-block tip" tabindex="0" data-toggle="tooltip" title="Inactive"><i class="fa fa-circle red" aria-hidden="true" value=${data}></i></span>`

				}

			},


		],
	});


	// Add event listener for opening and closing details
	$("#configuration_table tbody").on(
		"click",
		"td.details-control",
		function () {
			var td = $(this).closest('td');
			var tr = $(this).closest("tr");
			var row = table.row(tr);

			if (row.child.isShown()) {
				// This row is already open - close it
				td[0].innerHTML = '<i class="fas fa-angle-down color" aria-hidden="true"></i>';
				row.child.hide();
				tr.removeClass("shown");
			} else {
				// Open this row
				let websites_details = row.data().websites_details;
				if (websites_details.length > 0){
				    td[0].innerHTML = '<i class="fas fa-angle-up color" aria-hidden="true"></i>';
                    let row_html =
                        '<table class="table table-striped table-responsive table-bordered table-hover" cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
                        "<tr>" +
                        "<td class='url' style='width: 84.5%'>URL</td>" +
                        "<td class='price'>Desired Price</td>" +
                        "</tr>";

                    websites_details.forEach(function (row_data) {
                        row_html += format_child_row(row_data);
                    });

                    row_html += "</table>";

                    row.child(row_html).show();
                    tr.addClass("shown");
                }
			}
		}
	);


	/*------------------------------------Update Data---------------------------------*/
	

	$('#configuration_table tbody').on('click', 'td.active_state', function () {
		var td = $(this).closest('td');
		let html_object = $($(td[0].innerHTML)[0].innerHTML);
		let current_state = parseInt(html_object.attr('value'));
		console.log(current_state);
		var tr = $(this).closest('tr');
		var row = table.row(tr);
		let next_state = Pause;
		let state_html = `<span class="d-inline-block tip" tabindex="0" data-toggle="tooltip" title="Pause"><i class="fa fa-circle red" aria-hidden="true" value=${next_state}></i></span>`;
		if (current_state == Pause) {
			next_state = Resume;
			state_html = `<span class="d-inline-block tip" tabindex="0" data-toggle="tooltip" title="Resume"><i class="fa fa-circle green" aria-hidden="true" value=${next_state}></i></span>`;
		}
		td[0].innerHTML = state_html;

		configuration_id = row.data().configuration_id;

		dataString = {
			"configuration_id": configuration_id,
			"active_state": next_state
		}
		$.ajax({
			type: "PUT",
			dataType: "json",
			url: url + '/configuration/',
			contentType: "application/json",
			data: JSON.stringify(dataString), // serializes the form's elements.
			success: function (data) {
				// alert("Success: Data has been updated");
				swal("Data has been updated", "", "success");
				$('#configuration_table').DataTable().ajax.reload();
			},
			error: function (data) {
				swal("Data has not been updated");
			}
		});




	});




});







/*------------------------------------Post Data----------------------------------*/

$(submit_data).click(function (e) {
	// debugger;

	e.preventDefault(); // avoid to execute the actual submit of the form.

	let emails = [];
	let email_list = getValueByID("email"); // document.getElementById("email").value;
	let start_time = getValueByID("start_time"); //document.getElementById("start_time").value;
	let end_time = getValueByID("end_time"); //document.getElementById("end_time").value;
	// let start_time = moment(start_date).format('HH:mm:00');
	// let end_time = moment(end_date).format('HH:mm:00');
	let is_proxy = getValueByID("is_proxy"); //document.getElementById("is_proxy").value;
	let websites_details = [];
	let websites_no = parseInt(getValueByID("add_website"));

	let websites_no_list = range(1, websites_no);

	websites_no_list.forEach(function (index) {
		try {
			var url = getValueByID("website_" + index);
			var desired_price = getValueByID("desired_price_" + index);
	
			websites_details.push({
				url: url,
				desired_price: desired_price,
			});
		}
		catch (err) {

		}
	});

	emails = email_list.split(",").map(function (item) {
		return item.trim();
	});

	var dataString = {
		emails: emails,
		start_time: start_time,
		end_time: end_time,
		is_proxy: is_proxy,
		websites_details: websites_details,
	};

	// websites_details.map((item, index) => {
	// 	var reg = /\S*www\.\S+/;
	// 	if (reg.test(item.url)) {
	// 		return (
	// 			isWebValid = true
	// 		)
	// 	}
	// 	else {
	// 		return (
	// 			isWebValid = false
	// 		)
	// 	}
	// })


	for (var j = 0; j < emails.length; j++) {
		if (/@.*?\./.test(emails[j])) {
			isEmailValid = true;
		} else {
			isEmailValid = false;
			break;
		}
	}

	if (start_time < end_time) {
		isWebValid = true;
	}
	else {
		isEmailValid = false;
	}

	
	
	if (isWebValid && isEmailValid) {
		$.ajax({
			type: "POST",
			dataType: "json",
			url: url + '/configuration/',
			contentType: "application/json",
			data: JSON.stringify(dataString), // serializes the form's elements.
			success: function (data) {
				// alert("Success: Data has been added");
				swal("Data has been added", "", "success");
				$('#configuration_table').DataTable().ajax.reload();
				$('.form-control').val('') ;
				$('.form-control').val(''); 
				$('.add_btn').attr('disabled', true);
				let websites_no = parseInt(getValueByID("add_website"));

	            let websites_no_list = range(2, websites_no);
	            websites_no_list.forEach(function (index) {
                    try {
                        $("#row_" + index).remove();
//                        var url = getValueByID("website_" + index);
//                        var desired_price = getValueByID("desired_price_" + index);
//
//                        websites_details.push({
//                            url: url,
//                            desired_price: desired_price,
//                        });
                    }
                    catch (err) {

                    }
                });

			},
			error: function (data) {
				swal("Data has not been added");
				$('.form-control').val('') ;
				$('.form-control').val('');
			},
		});
	}
	else {
		$('.form-control').val('') ;
		$('.form-control').val(''); 
		// alert("Please enter valid credentials");
		swal("Please enter valid credentials");
	}
});


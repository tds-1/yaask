
var products = "",
	makes = "",
	models = "",
	types = "";

function add(data){
	for (var i = 0; i < data.length; i++) {
		var question = data[i].question,
			question_id = data[i].question_id,
			a = data[i].a,
			b = data[i].b,
			c = data[i].c,
			d = data[i].d,
			explanation = data[i].explanation
			answer = data[i].answer
			make = data[i].subject
			model = data[i].topic
			//create product cards

		products += "<div class=\"quests\" data-make='" + make + "' data-model='" + model + "'>\n" ;
		products += "<input type= \"checkbox\" "+ "id= \"" + question_id + "\" name=\" " + question_id + "\" value= \"checked\" >"

		products += "<label for=" + question_id + ">"
		products += "<table style =\"margin-bottom: 40px;\">\n\
			<tr>\n\
				<td>Question No. " + i+1 + "</td>\n\
				<td>Marks: 4</td>\n\
			</tr>\n\
			<tr>\n\
				<td colspan=\"2\">\n\
					"+question+"\n\
				</td >\n\
			</tr >\n\
			<tr>\n\
				<td>"+a+"</td>\n\
				<td>"+b+"</td>\n\
			</tr>\n\
			<tr>\n\
			<td>"+c+"</td>\n\
			<td>"+d+"</td>\n\
			</tr>\n\
			<tr>\n\
				<td colspan=\"2\"><b>Explanation</b>: "+explanation+" </td>\n\
			</tr>\n\
		</table>"
		products += "</label> \n </div>"

		//create dropdown of makes
		if (makes.indexOf("<option value='" + make + "'>" + make + "</option>") == -1) {
			makes += "<option value='" + make + "'>" + make + "</option>";
		}

		//create dropdown of models
		if (models.indexOf("<option value='" + model + "'>" + model + "</option>") == -1) {
			models += "<option value='" + model + "'>" + model + "</option>";
		}

		// //create dropdown of types
		// if (types.indexOf("<option value='" + type + "'>" + type + "</option>") == -1) {
		// 	types += "<option value='" + type + "'>" + type + "</option>";
		// }
	}
}

$(document).ready(function () {
    if (1) {
		$.ajax({
            type: "POST",
            url: "/quest",
            dataType: "json",
            success: function (temp) {
				add(temp);
				$("#quest").html(products);
				$(".filter-make").append(makes);
				$(".filter-model").append(models);
				$(".filter-type").append(types);
			
			}
        });
    }
});
var filtersObject = {};


//on search form submit'
function form_submit() {
	var f1 = document.getElementById("filter1").value;
	var f2 = document.getElementById("filter2").value;
	var f3 = document.getElementById("filter3").value;
	console.log(f1, f2, f3);
	if (f1 == "") {
		delete filtersObject["make"];
	} else {
		filtersObject["make"] = f1;
	}
	if (f2 == "") {
		delete filtersObject["model"];
	} else {
		filtersObject["model"] = f2;
	}
	if (f3 == "") {
		delete filtersObject["type"];
	} else {
		filtersObject["type"] = f3;
	}

	var filters = "";

	for (var key in filtersObject) {
		console.log(key);
		if (filtersObject.hasOwnProperty(key)) {
			filters += "[data-" + key + "='" + filtersObject[key] + "']";
		}
	}
	console.log(filters);
	if (filters == "") {
		$(".quests").show();
	} else {
		console.log("hide")
		$(".quests").hide();
		$(".quests").hide().filter(filters).show();
	}
}
$("#search-form").on('click', function (e) {
	e.preventDefault();
	console.log("hello");

	$(".quest").hide();
	$(".quest").each(function () {
		var make = $(this).data("make").toLowerCase(),
			model = $(this).data("model").toLowerCase(),
			type = $(this).data("type").toLowerCase();

		if (make.indexOf(query) > -1 || model.indexOf(query) > -1 || type.indexOf(query) > -1) {
			$(this).show();
		}
	});
});
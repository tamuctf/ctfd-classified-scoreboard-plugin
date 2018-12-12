$(document).ready(function(){
  $("select").trigger('change');
  $('.buttonCondition').prop('disabled', true); 
var toggler = document.getElementsByClassName("caret");
var i;

});



function updatescores() {
  if($('#classify').val() !== "ALL") {
      $.get(script_root + '/scores/' + $('#classify').val(), function(data) {
        teams = $.parseJSON(JSON.stringify(data));
        $('#scoreboard > tbody').empty()
        for (var i = 0; i < teams['standings'].length; i++) {
          row = "<tr><td>{0}</td><td><a href='/team/{1}'>{2}</a></td><td>{3}</td></tr>".format(i+1, teams['standings'][i].id, htmlentities(teams['standings'][i].team), teams['standings'][i].score)
          $('#scoreboard > tbody').append(row)
        };
      });
  } else {
    $.get(script_root + '/scores', function(data) {
      teams = $.parseJSON(JSON.stringify(data));
      $('#scoreboard > tbody').empty()
      for (var i = 0; i < teams['standings'].length; i++) {
        row = "<tr><td>{0}</td><td><a href='/team/{1}'>{2}</a></td><td>{3}</td></tr>".format(i+1, teams['standings'][i].id, htmlentities(teams['standings'][i].team), teams['standings'][i].score)
        $('#scoreboard > tbody').append(row)
      };
    });
  }
}

function scoregraph () {
  if($('#classify').val() === 'ALL') {
    $.get(script_root + '/top/10', function( data ) {
      var places = $.parseJSON(JSON.stringify(data));

      places = places['places'];
      if (Object.keys(places).length === 0 ){
          $('#score-graph').html('<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'); // Replace spinner
          return;
      }

      var teams = Object.keys(places);
      var traces = [];
      for(var i = 0; i < teams.length; i++){
          var team_score = [];
          var times = [];
          for(var j = 0; j < places[teams[i]]['solves'].length; j++){
              team_score.push(places[teams[i]]['solves'][j].value);
              var date = moment(places[teams[i]]['solves'][j].time * 1000);
              times.push(date.toDate());
          }
          team_score = cumulativesum(team_score);
          var trace = {
              x: times,
              y: team_score,
              mode: 'lines+markers',
              name: places[teams[i]]['name']
          };
          traces.push(trace);
      }

      traces.sort(function(a, b) {
          var scorediff = b['y'][b['y'].length - 1] - a['y'][a['y'].length - 1];
          if(!scorediff) {
              return a['x'][a['x'].length - 1] - b['x'][b['x'].length - 1];
          }
          return scorediff;
      });

      var layout = {
          title: 'Top 10 Teams',
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)'
      };

      $('#score-graph').empty(); // Remove spinners
      Plotly.newPlot('score-graph', traces, layout);
    });
  } else {
    $.get(script_root + '/top/10/'  + $('#classify').val(), function( data ) {
        var places = $.parseJSON(JSON.stringify(data));

        places = places['places'];
        if (Object.keys(places).length === 0 ){
            $('#score-graph').html('<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'); // Replace spinner
            return;
        }

        var teams = Object.keys(places);
        var traces = [];
        for(var i = 0; i < teams.length; i++){
            var team_score = [];
            var times = [];
            for(var j = 0; j < places[teams[i]]['solves'].length; j++){
                team_score.push(places[teams[i]]['solves'][j].value);
                var date = moment(places[teams[i]]['solves'][j].time * 1000);
                times.push(date.toDate());
            }
            team_score = cumulativesum(team_score);
            var trace = {
                x: times,
                y: team_score,
                mode: 'lines+markers',
                name: places[teams[i]]['name']
            };
            traces.push(trace);
        }

        traces.sort(function(a, b) {
            var scorediff = b['y'][b['y'].length - 1] - a['y'][a['y'].length - 1];
            if(!scorediff) {
                return a['x'][a['x'].length - 1] - b['x'][b['x'].length - 1];
            }
            return scorediff;
        });

        var layout = {
            title: 'Top 10 Teams',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)'
        };

        $('#score-graph').empty(); // Remove spinners
        Plotly.newPlot('score-graph', traces, layout);
    });
  }
}

function updatescores2() {
  if($('#tamu').val() !== 'ALL') {
      $.get(script_root + '/scores/' + $('#tamu').val(), function(data) {
        teams = $.parseJSON(JSON.stringify(data));
        $('#scoreboard > tbody').empty()
        for (var i = 0; i < teams['standings'].length; i++) {
          row = "<tr><td>{0}</td><td><a href='/team/{1}'>{2}</a></td><td>{3}</td></tr>".format(i+1, teams['standings'][i].id, htmlentities(teams['standings'][i].team), teams['standings'][i].score)
          $('#scoreboard > tbody').append(row)
        };
      });
  } else {
    $.get(script_root + '/scores', function(data) {
      teams = $.parseJSON(JSON.stringify(data));
      $('#scoreboard > tbody').empty()
      for (var i = 0; i < teams['standings'].length; i++) {
        row = "<tr><td>{0}</td><td><a href='/team/{1}'>{2}</a></td><td>{3}</td></tr>".format(i+1, teams['standings'][i].id, htmlentities(teams['standings'][i].team), teams['standings'][i].score)
        $('#scoreboard > tbody').append(row)
      };
    });
  }
}

function updatescores3() {
  if($('#tamum').val() !== 'ALL') {
      $.get(script_root + '/scores/' + $('#tamum').val(), function(data) {
        teams = $.parseJSON(JSON.stringify(data));
        $('#scoreboard > tbody').empty()
        for (var i = 0; i < teams['standings'].length; i++) {
          row = "<tr><td>{0}</td><td><a href='/team/{1}'>{2}</a></td><td>{3}</td></tr>".format(i+1, teams['standings'][i].id, htmlentities(teams['standings'][i].team), teams['standings'][i].score)
          $('#scoreboard > tbody').append(row)
        };
      });
  } else {
    $.get(script_root + '/scores', function(data) {
      teams = $.parseJSON(JSON.stringify(data));
      $('#scoreboard > tbody').empty()
      for (var i = 0; i < teams['standings'].length; i++) {
        row = "<tr><td>{0}</td><td><a href='/team/{1}'>{2}</a></td><td>{3}</td></tr>".format(i+1, teams['standings'][i].id, htmlentities(teams['standings'][i].team), teams['standings'][i].score)
        $('#scoreboard > tbody').append(row)
      };
    });
  }
}

function cumulativesum(arr) {
    var result = arr.concat();
    for (var i = 0; i < arr.length; i++){
        result[i] = arr.slice(0, i + 1).reduce(function(p, i){ return p + i; });
    }
    return result
}

function UTCtoDate(utc) {
    var d = new Date(0)
    d.setUTCSeconds(utc)
    return d;
}




function scoregraph2 () {
  if($('#tamu').val() === 'ALL') {
    $.get(script_root + '/top/10', function( data ) {
      var places = $.parseJSON(JSON.stringify(data));

      places = places['places'];
      if (Object.keys(places).length === 0 ){
          $('#score-graph').html('<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'); // Replace spinner
          return;
      }

      var teams = Object.keys(places);
      var traces = [];
      for(var i = 0; i < teams.length; i++){
          var team_score = [];
          var times = [];
          for(var j = 0; j < places[teams[i]]['solves'].length; j++){
              team_score.push(places[teams[i]]['solves'][j].value);
              var date = moment(places[teams[i]]['solves'][j].time * 1000);
              times.push(date.toDate());
          }
          team_score = cumulativesum(team_score);
          var trace = {
              x: times,
              y: team_score,
              mode: 'lines+markers',
              name: places[teams[i]]['name']
          };
          traces.push(trace);
      }

      traces.sort(function(a, b) {
          var scorediff = b['y'][b['y'].length - 1] - a['y'][a['y'].length - 1];
          if(!scorediff) {
              return a['x'][a['x'].length - 1] - b['x'][b['x'].length - 1];
          }
          return scorediff;
      });

      var layout = {
          title: 'Top 10 Teams',
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)'
      };

      $('#score-graph').empty(); // Remove spinners
      Plotly.newPlot('score-graph', traces, layout);
    });
  } else {
    $.get(script_root + '/top/10/'  + $('#tamu').val(), function( data ) {
        var places = $.parseJSON(JSON.stringify(data));

        places = places['places'];
        if (Object.keys(places).length === 0 ){
            $('#score-graph').html('<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'); // Replace spinner
            return;
        }

        var teams = Object.keys(places);
        var traces = [];
        for(var i = 0; i < teams.length; i++){
            var team_score = [];
            var times = [];
            for(var j = 0; j < places[teams[i]]['solves'].length; j++){
                team_score.push(places[teams[i]]['solves'][j].value);
                var date = moment(places[teams[i]]['solves'][j].time * 1000);
                times.push(date.toDate());
            }
            team_score = cumulativesum(team_score);
            var trace = {
                x: times,
                y: team_score,
                mode: 'lines+markers',
                name: places[teams[i]]['name']
            };
            traces.push(trace);
        }

        traces.sort(function(a, b) {
            var scorediff = b['y'][b['y'].length - 1] - a['y'][a['y'].length - 1];
            if(!scorediff) {
                return a['x'][a['x'].length - 1] - b['x'][b['x'].length - 1];
            }
            return scorediff;
        });

        var layout = {
            title: 'Top 10 Teams',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)'
        };

        $('#score-graph').empty(); // Remove spinners
        Plotly.newPlot('score-graph', traces, layout);
    });
  }
}

function scoregraph3 () {
  if($('#tamum').val() === 'ALL') {
    $.get(script_root + '/top/10', function( data ) {
      var places = $.parseJSON(JSON.stringify(data));

      places = places['places'];
      if (Object.keys(places).length === 0 ){
          $('#score-graph').html('<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'); // Replace spinner
          return;
      }

      var teams = Object.keys(places);
      var traces = [];
      for(var i = 0; i < teams.length; i++){
          var team_score = [];
          var times = [];
          for(var j = 0; j < places[teams[i]]['solves'].length; j++){
              team_score.push(places[teams[i]]['solves'][j].value);
              var date = moment(places[teams[i]]['solves'][j].time * 1000);
              times.push(date.toDate());
          }
          team_score = cumulativesum(team_score);
          var trace = {
              x: times,
              y: team_score,
              mode: 'lines+markers',
              name: places[teams[i]]['name']
          };
          traces.push(trace);
      }

      traces.sort(function(a, b) {
          var scorediff = b['y'][b['y'].length - 1] - a['y'][a['y'].length - 1];
          if(!scorediff) {
              return a['x'][a['x'].length - 1] - b['x'][b['x'].length - 1];
          }
          return scorediff;
      });

      var layout = {
          title: 'Top 10 Teams',
          paper_bgcolor: 'rgba(0,0,0,0)',
          plot_bgcolor: 'rgba(0,0,0,0)'
      };

      $('#score-graph').empty(); // Remove spinners
      Plotly.newPlot('score-graph', traces, layout);
    });
  } else {
    $.get(script_root + '/top/10/'  + $('#tamum').val(), function( data ) {
        var places = $.parseJSON(JSON.stringify(data));

        places = places['places'];
        if (Object.keys(places).length === 0 ){
            $('#score-graph').html('<div class="text-center"><h3 class="spinner-error">No solves yet</h3></div>'); // Replace spinner
            return;
        }

        var teams = Object.keys(places);
        var traces = [];
        for(var i = 0; i < teams.length; i++){
            var team_score = [];
            var times = [];
            for(var j = 0; j < places[teams[i]]['solves'].length; j++){
                team_score.push(places[teams[i]]['solves'][j].value);
                var date = moment(places[teams[i]]['solves'][j].time * 1000);
                times.push(date.toDate());
            }
            team_score = cumulativesum(team_score);
            var trace = {
                x: times,
                y: team_score,
                mode: 'lines+markers',
                name: places[teams[i]]['name']
            };
            traces.push(trace);
        }

        traces.sort(function(a, b) {
            var scorediff = b['y'][b['y'].length - 1] - a['y'][a['y'].length - 1];
            if(!scorediff) {
                return a['x'][a['x'].length - 1] - b['x'][b['x'].length - 1];
            }
            return scorediff;
        });

        var layout = {
            title: 'Top 10 Teams',
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)'
        };

        $('#score-graph').empty(); // Remove spinners
        Plotly.newPlot('score-graph', traces, layout);
    });
  }
}



function update() {
  updatescores();
  scoregraph();
}

function update2() {
  updatescores2();
  scoregraph2();
}

function update3() {
  updatescores3();
  scoregraph3();
}


setInterval(update, 300000); // Update scores every 5 minutes

window.onresize = function() {
  Plotly.Plots.resize(document.getElementById('score-graph'));
};


// -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
// TAMUctf Specific stuff

$(function () {
  $("#classify").change(function() {
    var val = $(this).val();
    if(val === "tamu") {
        $("#tamu").show();
        $("#tamum").hide();
    }
    else if(val === "tamum") {
        $("#tamum").show();
        $("#tamu").hide();
    }else if(val === "public") {
        $("#tamum").hide();
        $("#tamu").hide();
    }else if(val === "ALL") {
        $("#tamum").hide();
        $("#tamu").hide();
    }
  });
});

$("#dod").on("change", function() {
   if (document.getElementById("dod").checked){
    document.getElementById("rotc").checked = false
    document.getElementById("corps").checked = false
  }
});
$("#rotc").on("change", function() {
   if (document.getElementById("rotc").checked){
    document.getElementById("dod").checked = false
    document.getElementById("corps").checked = false
  }
});
$("#corps").on("change", function() {
   if (document.getElementById("corps").checked){
    document.getElementById("rotc").checked = false
    document.getElementById("dod").checked = false
  }
});


$("#bracketTable tbody tr").click(function(){
   $(this).addClass('selected').siblings().removeClass('selected');
    $('.buttonCondition').prop('disabled', false); 
});


$("#deleteForm").submit(function(){
  var selectedBracket = $(".selected").attr('name');
  var integer = parseInt(selectedBracket, 10);
  $("#submitDelete").val(integer);
});

$("#editButton").click(function(){
  var selectedBracket = $(".selected td").attr('name');
   // window.alert(selectedBracket);
  $("#bracket_name").val(selectedBracket);
});

$("#editForm").submit(function(){
  var selectedBracket = $(".selected").attr('name');
  var integer = parseInt(selectedBracket, 10);
  $("#editId").val(integer);
});

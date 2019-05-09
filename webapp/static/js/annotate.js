var lineOffset = 4;
var anchrSize = 3;
var gap = 50;

var mousedown = false;
var clickedArea = {
  box: -1,
  pos: 'o'
};
var x1 = -1;
var y1 = -1;
var x2 = -1;
var y2 = -1;
var mouseX, mouseY

var boxes = [];
var tmpBox = null;

// Highlight Selected
$('#detailTable').find('tr.field').click(function () {
  field_name = $(this).children('td:last-child').attr('id');
  $(this).parent().find('td').removeClass('highlight');
  $(this).children('td').addClass('highlight');
});

$('#detailTable').find('tr.field').first().click();

var canvas = document.getElementById("imgCanvas");
var wrapper = document.getElementById('canWrap');
var imageObj = new Image();
// imageObj.src = '../../../media/annotate/' + $('#pk').text() + '.png';
imageObj.src = '../../../static/media/annotate/' + $('#pk').text() + '.png';


getExistBoxese();

imageObj.onload = function () {
  image = imageObj;
  canvas.width = image.width + gap * 2;
  canvas.height = image.height + gap * 2;

  // Upsize canvas for smaller image
  if (canvas.width < wrapper.width) {
    canvas.width = wrapper.width - 10
  };
  if (canvas.height < wrapper.height) {
    canvas.height = wrapper.height - 10
  };
  redraw();
}

function redraw() {
  var context = canvas.getContext('2d');
  // CLEAR
  context.clearRect(0, 0, context.canvas.width, context.canvas.height);
  // Border
  context.lineWidth = 1;
  context.strokeStyle = 'black';
  context.strokeRect(gap - 1, gap - 1, image.width + 1, image.height + 1);
  // Image
  context.drawImage(image, gap, gap);
  // Boxes
  context.beginPath();
  // Clear Cordinate Table
  $('td.cor').empty();

  for (var i = 0; i < boxes.length; i++) {
    drawBoxOn(boxes[i], context);
    // Update Detail Table fields Status
    $('#' + boxes[i].name + '.cor').text('DONE');
    $('#' + boxes[i].name + '.cor').css({
      'color': 'red',
      'font-weight': 'bold'
    });

  }
  if (clickedArea.box == -1) {
    tmpBox = newBox(x1, y1, x2, y2);
    if (tmpBox != null && mousedown === true) {
      drawBoxOn(tmpBox, context);
    }
  }

  context.strokeStyle = 'red';
  // context.beginPath();
  context.moveTo(mouseX, 0);
  context.lineTo(mouseX, context.canvas.height);
  context.moveTo(0, mouseY);
  context.lineTo(context.canvas.width, mouseY);
  context.stroke();
  context.closePath();
}

canvas.onmousedown = function (e) {
  if (e.button === 0) {
    mousedown = true;
    clickedArea = findCurrentArea(e.offsetX, e.offsetY);
    mouseTransform(clickedArea);
    if (clickedArea.box != -1) {
      $('.cor#' + boxes[clickedArea.box].name).parent('tr').click();
    }
    x1 = e.offsetX;
    y1 = e.offsetY;
    x2 = e.offsetX;
    y2 = e.offsetY;
  }
};
canvas.onmouseup = function (e) {
  if (clickedArea.box == -1 && tmpBox != null) {
    boxes.forEach(function (box, i) {
      if (box.name == tmpBox.name) {
        boxes.splice(i, 1)
      }
    });
    boxes.push(tmpBox);

    // Jump to Next Field when finish Drawing if Next Field is Empty
    if ($('.cor.highlight').parent('tr').next('tr').children('td:last-child').is(':empty')) {
      $('.cor.highlight').parent('tr').next('tr').click();
    }
  } else if (clickedArea.box != -1) {
    var selectedBox = boxes[clickedArea.box];
    mouseTransform(selectedBox, [e.offsetX, e.offsetY]);
    if (selectedBox.x1 > selectedBox.x2) {
      var previousX1 = selectedBox.x1;
      selectedBox.x1 = selectedBox.x2;
      selectedBox.x2 = previousX1;
    }
    if (selectedBox.y1 > selectedBox.y2) {
      var previousY1 = selectedBox.y1;
      selectedBox.y1 = selectedBox.y2;
      selectedBox.y2 = previousY1;
    }
  };

  mouseTransform(clickedArea);
  clickedArea = {
    box: -1,
    pos: 'o'
  };
  tmpBox = null;
  mousedown = false;
  console.log(boxes);
};
canvas.onmouseout = function (e) {
  if (clickedArea.box != -1) {
    var selectedBox = boxes[clickedArea.box];
    if (selectedBox.x1 > selectedBox.x2) {
      var previousX1 = selectedBox.x1;
      selectedBox.x1 = selectedBox.x2;
      selectedBox.x2 > previousX1;
    }
    if (selectedBox.y1 > selectedBox.y2) {
      var previousY1 = selectedBox.y1;
      selectedBox.y1 = selectedBox.y2;
      selectedBox.y2 > previousY1;
    }
  };
  canvas.style.removeProperty('cursor');
  mousedown = false;
  clickedArea = {
    box: -1,
    pos: 'o'
  };
  tmpBox = null;
};
canvas.onmousemove = function (e) {
  if (mousedown && clickedArea.box == -1) {
    x2 = e.offsetX;
    y2 = e.offsetY;
    mouseX = x2
    mouseY = y2
    $('#imgCanvas').css({
      'cursor': 'crosshair'
    });
    redraw();
  } else if (mousedown && clickedArea.box != -1) {
    x2 = e.offsetX;
    y2 = e.offsetY;
    mouseX = x2
    mouseY = y2
    xOffset = x2 - x1;
    yOffset = y2 - y1;
    x1 = x2;
    y1 = y2;
    var index = clickedArea.box

    if (clickedArea.pos == 'i' ||
      clickedArea.pos == 'tl' ||
      clickedArea.pos == 'l' ||
      clickedArea.pos == 'bl') {
      boxes[index].x1 += xOffset;
    }
    if (clickedArea.pos == 'i' ||
      clickedArea.pos == 'tl' ||
      clickedArea.pos == 't' ||
      clickedArea.pos == 'tr') {
      boxes[index].y1 += yOffset;
    }
    if (clickedArea.pos == 'i' ||
      clickedArea.pos == 'tr' ||
      clickedArea.pos == 'r' ||
      clickedArea.pos == 'br') {
      boxes[index].x2 += xOffset;
    }
    if (clickedArea.pos == 'i' ||
      clickedArea.pos == 'bl' ||
      clickedArea.pos == 'b' ||
      clickedArea.pos == 'br') {
      boxes[index].y2 += yOffset;
    }

    // KEEP BOX inside CANVAS Image
    if (clickedArea.pos == 'i') {
      if (
        boxes[index].x1 < 0 ||
        boxes[index].x2 > imageObj.width
      ) {
        boxes[index].x1 -= xOffset;
        boxes[index].x2 -= xOffset;
      }
      if (
        boxes[index].y1 < 0 ||
        boxes[index].y2 > imageObj.height
      ) {
        boxes[index].y1 -= yOffset;
        boxes[index].y2 -= yOffset;
      }
    } else {
      if (
        boxes[index].x2 < 0 ||
        boxes[index].x2 > imageObj.height
      ) {
        boxes[index].x2 -= xOffset;
      }
      if (
        boxes[index].x1 < 0 ||
        boxes[index].x1 > imageObj.height
      ) {
        boxes[index].x1 -= xOffset;
      }
      if (
        boxes[index].y1 < 0 ||
        boxes[index].y1 > imageObj.height
      ) {
        boxes[index].y1 -= yOffset;
      }
      if (
        boxes[index].y2 < 0 ||
        boxes[index].y2 > imageObj.height
      ) {
        boxes[index].y2 -= yOffset;
      }
    }

    // Transform Mouse Cursor Style
    if (clickedArea.pos == 'i') {
      $('#imgCanvas').css({
        'cursor': 'grabbing',
        '-webkit-cursor': 'grabbing'
      })
    } else if (clickedArea.pos == 't' || clickedArea.pos == 'b') {
      $('#imgCanvas').css({
        'cursor': 'ns-resize'
      })
    } else if (clickedArea.pos == 'l' || clickedArea.pos == 'r') {
      $('#imgCanvas').css({
        'cursor': 'ew-resize'
      })
    } else {
      $('#imgCanvas').css({
        'cursor': 'all-scroll'
      })
    }

    redraw();
  } else if (mousedown === false) {
    mouseTransform(findCurrentArea(e.offsetX, e.offsetY));
    mouseX = e.offsetX
    mouseY = e.offsetY
    redraw();
  };
};

function mouseTransform(area) {
  if (area.box != -1) {
    if (area.pos == 'i') {
      canvas.style.cursor = 'grab';
      return;
    } else if (area.pos == 't' || area.pos == 'b') {
      canvas.style.cursor = 'ns-resize';
      return;
    } else if (area.pos == 'l' || area.pos == 'r') {
      canvas.style.cursor = 'ew-resize';
      return;
    } else if (area.pos == 'tl' || area.pos == 'br') {
      canvas.style.cursor = 'nwse-resize';
      return;
    } else if (area.pos == 'bl' || area.pos == 'tr') {
      canvas.style.cursor = 'nesw-resize';
      return;
    }
  } else {
    canvas.style.cursor = 'crosshair';
    return;
  }
};

function findCurrentArea(x, y) {
  for (var i = 0; i < boxes.length; i++) {
    var oriBox = boxes[i];
    box = unfixGap(oriBox);
    xCenter = box.x1 + (box.x2 - box.x1) / 2;
    yCenter = box.y1 + (box.y2 - box.y1) / 2;
    if (box.x1 - lineOffset < x && x < box.x1 + lineOffset) {
      if (box.y1 - lineOffset < y && y < box.y1 + lineOffset) {
        return {
          box: i,
          pos: 'tl'
        };
      } else if (box.y2 - lineOffset < y && y < box.y2 + lineOffset) {
        return {
          box: i,
          pos: 'bl'
        };
      } else if (yCenter - lineOffset < y && y < yCenter + lineOffset) {
        return {
          box: i,
          pos: 'l'
        };
      }
    } else if (box.x2 - lineOffset < x && x < box.x2 + lineOffset) {
      if (box.y1 - lineOffset < y && y < box.y1 + lineOffset) {
        return {
          box: i,
          pos: 'tr'
        };
      } else if (box.y2 - lineOffset < y && y < box.y2 + lineOffset) {
        return {
          box: i,
          pos: 'br'
        };
      } else if (yCenter - lineOffset < y && y < yCenter + lineOffset) {
        return {
          box: i,
          pos: 'r'
        };
      }
    } else if (xCenter - lineOffset < x && x < xCenter + lineOffset) {
      if (box.y1 - lineOffset < y && y < box.y1 + lineOffset) {
        return {
          box: i,
          pos: 't'
        };
      } else if (box.y2 - lineOffset < y && y < box.y2 + lineOffset) {
        return {
          box: i,
          pos: 'b'
        };
      } else if (box.y1 - lineOffset < y && y < box.y2 + lineOffset) {
        return {
          box: i,
          pos: 'i'
        };
      }
    } else if (box.x1 - lineOffset < x && x < box.x2 + lineOffset) {
      if (box.y1 - lineOffset < y && y < box.y2 + lineOffset) {
        return {
          box: i,
          pos: 'i'
        };
      }
    }
  }
  return {
    box: -1,
    pos: 'o'
  };
};

function newBox(x1, y1, x2, y2) {
  boxX1 = (x1 < x2) ? x1 : x2;
  boxY1 = (y1 < y2) ? y1 : y2;
  boxX2 = (x1 > x2) ? x1 : x2;
  boxY2 = (y1 > y2) ? y1 : y2;
  if (boxX2 - boxX1 > lineOffset * 2 && boxY2 - boxY1 > lineOffset * 2) {
    fixBox = fixGap(boxX1, boxX2, boxY1, boxY2);
    return {
      x1: fixBox.x1,
      y1: fixBox.y1,
      x2: fixBox.x2,
      y2: fixBox.y2,
      name: field_name,
    };
  } else {
    return null;
  }
};

function drawBoxOn(box, context) {
  cor = unfixGap(box)

  xCenter = cor.x1 + (cor.x2 - cor.x1) / 2;
  yCenter = cor.y1 + (cor.y2 - cor.y1) / 2;

  context.strokeStyle = 'DeepSkyBlue';
  context.lineWidth = 1;
  context.rect(cor.x1, cor.y1, (cor.x2 - cor.x1), (cor.y2 - cor.y1));
  context.stroke();

  context.fillStyle = 'rgba(0,0,0,0.1)';
  context.fillRect(cor.x1, cor.y1, (cor.x2 - cor.x1), (cor.y2 - cor.y1));

  context.fillStyle = 'DeepSkyBlue';
  context.fillRect(cor.x1 - anchrSize, cor.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(cor.x1 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(cor.x1 - anchrSize, cor.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, cor.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(xCenter - anchrSize, cor.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(cor.x2 - anchrSize, cor.y1 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(cor.x2 - anchrSize, yCenter - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillRect(cor.x2 - anchrSize, cor.y2 - anchrSize, 2 * anchrSize, 2 * anchrSize);
  context.fillStyle = "red";
  context.textAlign = "right";
  context.font = "13px Roboto";
  context.fillText(up_space(box.name), cor.x2 - 4, cor.y2 - 4);
};

function fixGap(x1, x2, y1, y2) {
  x1 = x1 - gap;
  x2 = x2 - gap;
  y1 = y1 - gap;
  y2 = y2 - gap;

  function fixX(x) {
    if (x < 0) {
      return 0
    } else if (x > imageObj.width) {
      return imageObj.width
    } else {
      return x
    }
  }

  function fixY(y) {
    if (y < 0) {
      return 0
    } else if (y > imageObj.height) {
      return imageObj.height
    } else {
      return y
    }
  }

  return {
    x1: fixX(x1),
    x2: fixX(x2),
    y1: fixY(y1),
    y2: fixY(y2),
  }
};

function unfixGap(box) {
  return {
    x1: box.x1 + gap,
    y1: box.y1 + gap,
    x2: box.x2 + gap,
    y2: box.y2 + gap
  }
};

// Navigate A - D, Prev - Next
document.addEventListener("keydown", function (event) {
  if (event.keyCode == 65) {  // A
    $('.cor.highlight').parent('tr').prev('tr').click();
  } else if (event.keyCode == 68) {  // D
    $('.cor.highlight').parent('tr').next('tr').click();
  } else if (event.keyCode == 88) {  // X
    for (var i = 0; i < boxes.length; i++) {
      if (boxes[i]['name'] === $('.cor.highlight').attr('id')) {
        console.log('Remove field', boxes[i]);
        boxes.splice(i, 1);
      };
      redraw();
    };
    // console.log(boxes);
  }
})

function up_space(str) {
  return replaceAll(str.toUpperCase(), "_", " ")
}

function replaceAll(str, find, replace) {
  return str.replace(new RegExp(find, 'g'), replace);
}

// Submit
$('#submit-button').click(function () {
  console.log('$&$ submiting ANNOTATED $&$');
  getSpinnerDimmed();

  var fields = {};
  for (var i = 0; i < boxes.length; i++) {
    f_name = boxes[i]['name']
    fields[f_name] = {
      x1: boxes[i].x1,
      x2: boxes[i].x2,
      y1: boxes[i].y1,
      y2: boxes[i].y2
    };
  };
  ajax_submiting(fields); 
});

function ajax_submiting(f_data) {
  console.log("$&$ Submiting Annotate Cordinate $&$");
  $.ajax({
    url: "/annotation/process/" + $("#pk").text() + "/",
    type: "POST",
    data: JSON.stringify(f_data),
    dataType: "json",
    success: function(data) {
      console.log("$&$ Submiting SUCCESS $&$");
      toastr.success(
        "SI Annotation has been successfully submitted",
        "SUCCESS"
      );
      window.location.href = "/drafting/index/";
    },

    error: function(data) {
      console.log("$&$ Submiting FALSE $&$");
      toastr.warning("SI Annotation submittion is FALSE", "ERROR");
      console.log(data);
    },

    complete: function() {
      console.log("$&$ Submiting COMPLETED $&$");
    }
  });
}

function getSpinnerDimmed() {
  console.log('$ GETTING Spin Dimmed Loader $');
  // dimmed blanket
  $('#main-content').wrap('<div class="dimmed" style="pointer-events: none;"></div>');
  // loader
  $("#main-content").append(
    '<div class="lds-spinner"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>'
  );
  $('.lds-spinner').css('top', ($(window).height() - $(".lds-spinner").height()) / 2);
  $('.lds-spinner').css('left', ($(window).width() - $(".lds-spinner").width()) / 2);
  $(".dimmed").css("position", "inherit");
}

function getExistBoxese() {
  $('#existCor').find('tr').each((i, elm) => {
    boxes.push({
      x1: parseInt($(elm).children("td.fX1").text()),
      y1: parseInt($(elm).children("td.fY1").text()),
      x2: parseInt($(elm).children("td.fX2").text()),
      y2: parseInt($(elm).children("td.fY2").text()),
      name: $(elm).children("td.fName").text()
    });
  });
}

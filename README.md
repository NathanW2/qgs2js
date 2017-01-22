## exp2js

Converts a QGIS Expression string into a JS function.

Work in progress...

Main ussage at the moment is for qgis2web (https://github.com/tomchadwin/qgis2web) by Tom 

## Usage

There is none yet... Main API entry point is `exp2func`

## Example

Work in progress examples

```javascript
//NOT var('myvar') = format('some string %1 %2', 'Hello', 'World')
function gwly_eval_expression(context) {
    var feature = context.feature;
    
    return ! (fnc_var(['myvar'], context) == fnc_format(['some string %1 %2','Hello','World'], context)) ;
}

gwly_eval_expression(context);

//CASE WHEN to_int(123.52) = var('myvar') THEN to_real(123) WHEN 1 + 2 = 3 THEN 2 ELSE to_int(1) END OR 2 * 2 + 5 = 4
function bzni_eval_expression(context) {
    var feature = context.feature;
    function _CASE() {
    if (fnc_to_int([123.52], context) == fnc_var(['myvar'], context)) {
          return fnc_to_real([123], context);
        }
        else if ((1 + 2) == 3) {
          return 2;
        }
    else {
     return fnc_to_int([1], context);
    }
    };
    return (_CASE() || (((2 * 2) + 5) == 4));
}

bzni_eval_expression(context);


```



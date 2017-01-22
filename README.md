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
function xtjs_eval_expression(context) {
    var feature = context.feature;
    
    return ! (fnc_var(['myvar'], context) == fnc_format(['some string %1 %2','Hello','World'], context)) ;
}

xtjs_eval_expression(context);

//CASE WHEN 1 = 1 THEN 1 WHEN 1 = 2 THEN 2 ELSE 1 END OR 2 * 2 + 5 = 4
function hiel_eval_expression(context) {
    var feature = context.feature;
    function _CASE() {
    if (1 == 1) {
          return 1;
        }
        else if (1 == 2) {
          return 2;
        }
    else {
     return null;
    }
    };
    return (_CASE() || (((2 * 2) + 5) == 4));
}

hiel_eval_expression(context);

```



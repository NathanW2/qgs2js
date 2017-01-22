## exp2js

Converts a QGIS Expression string into a JS function.

Work in progress...

Main ussage at the moment is for qgis2web (https://github.com/tomchadwin/qgis2web) by Tom 

## Usage

There is none yet... Main API entry point is `exp2func`

`gen_func_stubs` will generate function stubs for all registered QGIS functions at the time.

## Example

Work in progress examples

```javascript
var feature = {
            COLA: 1,
            COLB: 2,
            WAT: 'Hello World'
        };

var context = {
            feature: feature,
            variables: {}
        };


function ueun_eval_expression(context) {
    // NOT var('myvar') = format('some string %1 %2', 'Hello', 'World')

    var feature = context.feature;
    
    return ! (fnc_var(['myvar'], context) == fnc_format(['some string %1 %2','Hello','World'], context)) ;
}

var result = ueun_eval_expression(context);
console.log(result);


function rgpj_eval_expression(context) {
    // CASE WHEN to_int(123.52) = var('myvar') THEN to_real(123) WHEN 1 + 2 = 3 THEN 2 ELSE to_int(1) END OR 2 * 2 + 5 = 4

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

var result = rgpj_eval_expression(context);
console.log(result);


function ppwa_eval_expression(context) {
    // CASE WHEN COLA = 1 THEN 1 WHEN 1 + 2 = 3 THEN 2 ELSE 3 END

    var feature = context.feature;
    function _CASE() {
    if (feature['COLA']  == 1) {
          return 1;
        }
        else if ((1 + 2) == 3) {
          return 2;
        }
    else {
     return 3;
    }
    };
    return _CASE();
}

var result = ppwa_eval_expression(context);
console.log(result);

```



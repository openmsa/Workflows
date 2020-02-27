<?php

require_once LIBRARY_DIR . 'Smarty/Smarty.class.php';
require_once LIBRARY_DIR . 'smarty_functions.php';
require_once LIBRARY_DIR . 'smarty_modifiers.php';

/**
 * Resolve a template using variables, functions and modifiers
 * @param unknown $template         Template content to resolve
 * @param string $vars              Array of name,value pairs used to resolve the template
 * @param string $smarty_plugins    type indexed arrays of plugins (see http://www.smarty.net/docs/en/api.register.plugin.tpl)
 * Plugin types are: 'function', 'modifier', 'block'
 */
function resolve_template_var($template, $vars = null, $smarty_plugins = null)
{
  global $sms_smarty_template;

  try
  {
    $name = md5($template);
    $sms_smarty_template[$name] = $template;
    return resolve_template_internal("var:$varname", $vars, $smarty_plugins);
  }
  catch (Exception $e)
  {
    logToFile($e->getMessage());
    $obj_cmd = substr($varname, 0, strrpos($varname, '_'));
    if (empty($obj_cmd))
    {
      throw $e;
    }
    $parts = preg_split('/_/', $obj_cmd);
    $obj_cmd = "{$parts[1]} of {$parts[0]}.xml";
    $msg = str_replace("\"var:$varname\"", $obj_cmd, $e->getMessage());
    throw new Exception($msg, ERR_LOCAL_TEMPLATE, $e);
  }
}

/**
 * Resolve a template file using the configuration variables
 *
 * @param $template_path
 * @param string $vars              Array of name,value pairs used to resolve the template
 * @param string $smarty_plugins    type indexed arrays of plugins (see http://www.smarty.net/docs/en/api.register.plugin.tpl)
 * Plugin types are: 'function', 'modifier', 'block'
 */
function resolve_template_file($template_path, $vars = null, $smarty_plugins = null)
{
  try
  {
    return resolve_template_internal("file:$template_path", $vars, $smarty_plugins);
  }
  catch (Exception $e)
  {
    logToFile($e->getMessage());
    return file_get_contents($template_path);
  }
}

/* internal */
function var_get_template($tpl_name, &$tpl_source, $smarty_obj)
{
  global $sms_smarty_template;

  $tpl_source = $sms_smarty_template[$tpl_name];
  return true;
}

/* internal */
function var_get_timestamp($tpl_name, &$tpl_timestamp, $smarty_obj)
{
  global $sms_smarty_time;
  if (!isset($sms_smarty_time))
  {
    $sms_smarty_time = time();
  }
  else
  {
    $sms_smarty_time = $sms_smarty_time + 1;
  }
  $tpl_timestamp = $sms_smarty_time; // this example will always recompile!
  return true;
}

/* internal */
function var_get_secure($tpl_name, $smarty_obj)
{
  // assume all templates are secure
  return true;
}

/* internal */
function var_get_trusted($tpl_name, $smarty_obj)
{
  // not used for templates
}

/* internal */
function resolve_template_internal($resource_template, $additional_vars = null, $smarty_plugins = null)
{
  global $_smarty_fct;
  global $_smarty_mod;
  global $resolve_template_error;
  global $context;

  // Empty last error
  @trigger_error('');
  $resolve_template_error = '';

  $smarty = new Smarty();
  $smarty->compile_check = true;
  $smarty->compile_dir = '/opt/ubi-jentreprise/smartyc';
  $smarty->compile_id = uniqid("process_", true);
  $smarty->caching = false;
  $smarty->registerResource('var', array(
      'var_get_template',
      'var_get_timestamp',
      'var_get_secure',
      'var_get_trusted'));

  if (!empty($smarty_plugins))
  {
    foreach ($smarty_plugins as $type => $plugins)
    {
      foreach ($plugins as $name => $function)
      {
        $smarty->registerPlugin($type, $name, $function, false);
      }
    }
  }

  if (!empty($_smarty_fct))
  {
    foreach ($_smarty_fct as $name => $function)
    {
      $smarty->registerPlugin('function', $name, $function, false);
    }
  }

  if (!empty($_smarty_mod))
  {
    foreach ($_smarty_mod as $name => $function)
    {
      $smarty->registerPlugin('modifier', $name, $function, false);
    }
  }

  if (!empty($context))
  {
    foreach ($context as $name => $value)
    {
      $smarty->assign($name, $value);
    }
  }

  if (!empty($additional_vars))
  {
    //debug_dump($additional_vars, "ADDITIONNAL VARS\n");
    foreach ($additional_vars as $name => $value)
    {
      $smarty->assign($name, $value);
    }
  }

  try
  {
    $resolved_template = $smarty->fetch("$resource_template");
  }
  catch (Exception $e)
  {
    trigger_error($e->getMessage());
    $err = error_get_last();
    if ($err !== null && !empty($err['message']))
    {
      $resolve_template_error = $err['message'];
    }
    $smarty->clearCompiledTemplate(null, null, 100);
    throw $e;
  }
  $err = error_get_last();
  if ($err !== null && !empty($err['message']))
  {
    $resolve_template_error = $err['message'];
  }

  $smarty->clearCompiledTemplate(null, null, 100);

  return $resolved_template;
}


?>
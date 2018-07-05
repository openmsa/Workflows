<?php
/*
 * Version: $Id$
 * Created: Apr 28, 2011
 */

// Functions to be used in objects smarty templates
$_smarty_fct['get_mask_len'] = 'smarty_function_get_mask_len';
$_smarty_fct['get_mask_from_len'] = 'smarty_function_get_mask_from_len';
$_smarty_fct['invert_mask'] = 'smarty_function_invert_mask';
$_smarty_fct['urlencode'] = 'smarty_function_urlencode';

/**
 * Convert a network mask (255.255.255.0) into a length (24)
 * @param unknown $params
 * @param Smarty_Internal_Template $template
 * @return mask length
 */
function smarty_function_get_mask_len($params, Smarty_Internal_Template $template)
{
  $mask = $params['mask'];
  if (empty($mask))
  {
    return 32;
  }

  $masknum = ip2long($mask);
  $len = 0;
  if ($masknum !== 0)
  {
    while (($masknum & 0x00000001) === 0)
    {
      $masknum = ($masknum >> 1) & 0x7FFFFFFF;
    }
    while (($masknum & 0x00000001) === 1)
    {
      $masknum = ($masknum >> 1) & 0x7FFFFFFF;
      $len += 1;
    }
  }

  if (!empty($params['var']))
  {
    $template->assign($params['var'], $len);
  }

  return $len;
}

/**
 * Convert a network mask (255.255.255.0) into a length (24)
 * @param unknown $params
 * @param Smarty_Internal_Template $template
 * @return netmask
 */
function smarty_function_get_mask_from_len($params, Smarty_Internal_Template $template)
{
  $len = $params['len'];
  if (empty($len))
  {
    return '0.0.0.0';
  }

  $lmask = 0xFFFFFFFF;
  for ($i = 0; $i < (32 - $len); $i++)
  {
    $lmask = $lmask << 1;
  }

  $mask = long2ip($lmask & 0xFFFFFFFF);

  if (!empty($params['var']))
  {
    $template->assign($params['var'], $mask);
  }

  return $mask;
}

/**
 * Invert network mask 255.255.255.0 => 0.0.0.255
 * @param unknown $params
 * @param Smarty_Internal_Template $template
 * @return inverted mask
 */
function smarty_function_invert_mask($params, Smarty_Internal_Template $template)
{
  $mask = $params['mask'];

  if (empty($mask))
  {
    return '0.0.0.0';
  }

  $masknum = ip2long($mask);
  $inverted_mask = ~$masknum;

  $imask = long2ip($inverted_mask);
  if (!empty($params['var']))
  {
    $template->assign($params['var'], $imask);
  }

  return $imask;
}

/**
 * Encode URL
 * @param unknown $params
 * @param Smarty_Internal_Template $template
 * @return inverted mask
 */
function smarty_function_urlencode($params, Smarty_Internal_Template $template)
{
  $url = $params['url'];
  return urlencode($url);
}

?>

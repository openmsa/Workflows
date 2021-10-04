from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()
context = Variables.task_call()

# (1) loopbacks
ms_left_loopback_vars = {"object_id": context['id'],
                         "ip_address": context['leftsubnet']
                         }

sdwan_loopback_left = {"sdwan_loopback":
                       {context['id']: ms_left_loopback_vars}
                       }

ms_right_loopback_vars = {"object_id": context['id'],
                          "ip_address": context['rightsubnet']
                          }

sdwan_loopback_right = {"sdwan_loopback":
                        {context['id']: ms_right_loopback_vars}
                        }

# (2) secrets
ms_left_secret_vars = {"object_id": context['id'],
                       "left": context['left_device_ip'],
                       "right": context['right_device_ip'],
                       "secret": context['secret'],
                       }

sdwan_ipsec_secret_left = {"sdwan_ipsec_secret":
                           {context['id']: ms_left_secret_vars}
                           }

ms_right_secret_vars = {"object_id": context['id'],
                        "left": context['right_device_ip'],
                        "right": context['left_device_ip'],
                        "secret": context['secret'],
                        }

sdwan_ipsec_secret_right = {"sdwan_ipsec_secret":
                            {context['id']: ms_right_secret_vars}
                            }

# (3) global policy

ms_global_policy_vars = {"object_id": context['id'],
                         "ikelifetime": "1440m",
                         "keylife": "60m",
                         "rekeymargin": "3m",
                         "keyingtries": "1",
                         "keyexchange": "ikev1",
                         "authby": "secret"
                         }

sdwan_ipsec_conf_left = {"sdwan_ipsec_conf":
                         {context['id']: ms_global_policy_vars}
                         }

sdwan_ipsec_conf_right = {"sdwan_ipsec_conf":
                          {context['id']: ms_global_policy_vars}
                          }

# (4) crypto_maps

ms_left_cryptomap_vars = {"object_id": context['id'],
                          "left": context['left_device_ip'],
                          "right": context['right_device_ip'],
                          "leftsubnet": context['leftsubnet'],
                          "rightsubnet": context['rightsubnet'],
                          "ike": "aes128-md5-modp1536",
                          "esp": "aes128-sha1",
                          "leftid": context['left_device_ip'],
                          "rightid": context['right_device_ip'],
                          "leftfirewall": "yes",
                          "auto": "start"
                          }

sdwan_ipsec_conf_crypto_map_left = {"sdwan_ipsec_conf_cryptomap":
                                    {context['id']: ms_left_cryptomap_vars}
                                    }

ms_right_cryptomap_vars = {"object_id": context['id'],
                           "left": context['right_device_ip'],
                           "right": context['left_device_ip'],
                           "leftsubnet": context['rightsubnet'],
                           "rightsubnet": context['leftsubnet'],
                           "ike": "aes128-md5-modp1536",
                           "esp": "aes128-sha1",
                           "leftid": context['right_device_ip'],
                           "rightid": context['left_device_ip'],
                           "leftfirewall": "yes",
                           "auto": "start"
                           }
sdwan_ipsec_conf_crypto_map_right = {"sdwan_ipsec_conf_cryptomap":
                                     {context['id']: ms_right_cryptomap_vars}
                                     }

context["sdwan_loopback_left"] = sdwan_loopback_left
context["sdwan_loopback_right"] = sdwan_loopback_right
context["sdwan_ipsec_secret_left"] = sdwan_ipsec_secret_left
context["sdwan_ipsec_secret_right"] = sdwan_ipsec_secret_right
context["sdwan_ipsec_conf_left"] = sdwan_ipsec_conf_left
context["sdwan_ipsec_conf_right"] = sdwan_ipsec_conf_right
context["sdwan_ipsec_conf_crypto_map_left"] = sdwan_ipsec_conf_crypto_map_left
context["sdwan_ipsec_conf_crypto_map_right"] = sdwan_ipsec_conf_crypto_map_right


ret = MSA_API.process_content('ENDED',
                              f'IPsec data prepared {context["sdwan_loopback_left"]}',
                              context, True)

print(ret)
